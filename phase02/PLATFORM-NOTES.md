# GitCode 平台实测笔记（Phase 02 执行前必读）

> 本文件记录在真实测试仓库 `ComputingActionTest/foundational-tests` 上跑通一个最小用例时，
> 实测确认的平台行为。**平台行为 ≠ 官方文档**——凡冲突，以本文件的实测为准。
> 每条都带证据（pilot run 号）。最后更新：2026-07-21。

---

## 0. 已跑通的最小基线（GREEN 模板）

以下 workflow 实测 **COMPLETED（绿）**——`PILOT-BASIC` run#1，手动触发，14s 级：

```yaml
name: PILOT-BASIC
on:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  basic:
    name: basic                          # job 必须有 name
    runs-on: [ubuntu-latest, x64, small] # 数组，不是 {花括号}
    steps:
      - name: Checkout source            # 每个 step 必须有 name
        uses: checkout                   # 裸插件名，不是 official_checkout / actions/checkout@v4
      - name: Run and assert
        run: |                           # 一律 block scalar，哪怕单行
          echo "BASIC_OK: reached run step"
          echo "DONE_MARKER: completed"
```

编译 workflow 时以此为骨架。格式细则见 `phase01/schema/VALIDATION-RULES.md` §1–§4c。

---

## 1. 格式规则（实测确认，冲突以此为准）

| 规则 | 实测结论 | 证据 |
|---|---|---|
| `runs-on` | **数组** `[ubuntu-latest, x64, small]`；官方 examples/ 的 `{ubuntu-24,x64,small}` 花括号会被拒 | USE-DOC-02-003 #2 用数组 COMPLETED |
| `uses` | **裸插件名** `checkout`/`setup-node`/`cache`…；`official_` 前缀、`actions/xxx@v4` 都非法（除非负向测 GitHub 格式） | using-actions.md + 校验通过 |
| `if:` 状态 | **只认 `${{ always() }}`（带括号）**。裸 `${{ always }}`/`${{ failed }}`（文档写法）与 `${{ success() }}` 全被拒 | PILOT-FORMAT-CHECK #2/#3 网页校验错误 |
| success/failure 门控 | **暂无确认可用写法**——别用状态门控，条件改用 `${{ atomgit.* }}` 显式表达式或 job `needs` | 同上，success()/裸 failed 均被拒 |
| `run:` | **一律 `run: \|` block scalar**。单行含冒号 → `Nested mappings are not allowed in compact mappings` | PILOT-FORMAT-CHECK line-19 报错，改块标量后消失 |
| job/step name | 都必填；step name 禁 `[ ] \| $ { }` 等字符 | VALIDATION-RULES §2/§3 |

> ⚠️ 官方文档 `configure-conditional-execution.md` 写裸关键字 `${{ always }}`，但部署校验器不认——
> **文档在 `if:` 状态这块是错的。** 曾据文档误把规则改成裸关键字，实测后已改回 `always()`。

---

## 2. 触发方式（★ 批量执行的关键约束，尚未完全解决）

实测铁证：

| run | event | 结果 |
|---|---|---|
| PILOT-BASIC #1 | **Manual**（手动触发） | ✅ COMPLETED |
| USE-DOC-02-003 #2 | **Manual** | ✅ COMPLETED |
| USE-DOC-02-003 #1、hello ×5、comp-*、pilot-* 全部 | **PUSH** | ❌ ~1s 失败 / 不创建 run |

**结论：在此仓库，push 不会（可靠地）自动触发流水线，只有手动触发 / `workflow_dispatch` 能真正跑起来。**

未解决 / 待定（`workflow-runner.md` 阶段二依赖）：
- 手动触发目前只能在**网页 UI 登录后**点「运行工作流」；PAT 只能读、不能触发。
- 找过的 `workflow_dispatch` API 全部 404（v8/v5 各种路径均试过）。
- **批量 249 条的触发方式必须先定**：要么修 runner 让 push 自动跑，要么拿到平台真正的 dispatch 接口。

---

## 3. API 访问（api-client 固化）

```bash
TOKEN="<PAT>"
BASE="https://api.gitcode.com/api/v8/repos/<owner>/<repo>/actions"

# 认证：Authorization: Bearer（不是 access_token 查询参数）
# 列 run：per_page=10 较稳；部分节点偶发 PARAMETER_ERROR(codeArtsIds)，需重试
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/runs?per_page=10"

# 关键字段：status(COMPLETED/FAILED)、event(Manual/PUSH)、workflow_run_id
# run 详情 / jobs：
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/runs/<run_id>"
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/runs/<run_id>/jobs"
```

⚠️ **校验错误（Validation Error）只在网页 UI 显示**，v8 API 的 run `message` 字段是 `null`。
用例 workflow 编译失败时，job 数为 0、`event=PUSH`、耗时 1s——去网页 run 详情页看
「N 个错误」才能拿到具体报错。这是调试编译问题的唯一途径。

---

## 4. 复用脚本片段

列最近 run（含重试穿透 PARAMETER_ERROR）：

```bash
for i in $(seq 1 15); do
  curl -s -H "Authorization: Bearer $TOKEN" "$BASE/runs?per_page=10" > /tmp/r.json 2>/dev/null
  if python3 -c "import json,sys;sys.exit(0 if 'workflow_runs' in json.load(open('/tmp/r.json')) else 1)" 2>/dev/null; then
    python3 -c "import json;[print(r['run_number'],r['status'],r['event'],r['workflow_name']) for r in json.load(open('/tmp/r.json'))['workflow_runs']]"
    break
  fi; sleep 3
done
```
