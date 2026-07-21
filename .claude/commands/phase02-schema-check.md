# /phase02-schema-check — 校验 Phase 01 输入的 YAML 用例

## 用途
Phase 02 的第一道闸门。对 Phase 01 产出的可执行 YAML 用例逐条做 schema 校验，通过的进入执行队列，不通过的生成拒收清单回报 Phase 01。

## 何时使用
- Phase 01 完成一批用例产出后（`/phase01-gen` DoD），准备执行前
- Phase 01 重新编译 YAML 后（`/phase01-compile`），重新校验
- 怀疑某些 YAML 可能不符合 schema 时

## 前置条件
- Phase 01 的 `runs/<run-id>/cases/yaml/` 目录下有 `.yaml` 文件
- `phase01/schema/executable-case.schema.yaml` 可用
- 已确认目标 Phase 01 run-id

## 执行步骤

1. **确认输入源**：询问用户目标 Phase 01 run-id（如 `2026-07-20-01`）。若用户未指定，扫描 `phase01/runs/` 下最新的 delivered run。

2. **读取 schema**：读 `phase01/schema/executable-case.schema.yaml`，解析所有 required 字段、类型约束、枚举值、正则 pattern。

3. **逐条校验**（参照 `phase02/scripts/schema-validator.md` 规格）：
   - 扫描 `phase01/runs/<run-id>/cases/yaml/*.yaml`
   - 逐条检查：
     - 文件可解析为合法 YAML
     - 必填字段齐全：`id`, `dimensions`, `dimension`, `priority`, `title`, `intent_ref`, `setup`, `trigger`, `assertions`, `teardown`
     - `id` 符合格式 `^(COMP|COMPAT|REL|SEC|USE)-[A-Z0-9]+-\d{2}-\d{3}(-V\d+)?$`
     - `dimension` 在枚举值内
     - `priority` 在 `[P0, P1, P2]` 内
     - `trigger.event` 在 `[push, pr, fork_pr, manual, schedule, tag]` 内
     - `assertions[].type` 在 `[positive, negative, nonfunctional]` 内
     - `teardown.reset` 在 `[fixture, full_instance, none]` 内
   - 业务校验：
     - `dimension=security` 的用例，`assertions` 中至少一条 `type=negative`
     - `fault_injection != null` 且 `teardown.reset=none` → 警告（破坏性用例应声明清理级别）

4. **输出结果**：
   - 通过的用例：写入 `phase02/runs/<run-id>/queue.md`
   - 不通过的用例：写入 `phase02/runs/<run-id>/rejected.md`（格式见 `contract.md` §4.2）
   - 终端输出：通过/拒收数量统计

5. **门禁判断**：
   - 全部通过 → 可以执行 `/phase02-exec`
   - 有拒收 → **阻止执行**，将拒收清单抄送用户，等待 Phase 01 修复后重校验

## 输出
- `phase02/runs/<run-id>/queue.md` — 执行队列
- `phase02/runs/<run-id>/rejected.md` — 拒收清单
- `phase02/runs/<run-id>/run.md` — 初始化元信息

## 示例
```
/phase02-schema-check                    # 自动选最新 Phase 01 run
/phase02-schema-check 2026-07-20-01      # 指定 Phase 01 run-id
```

---

## YAML 校验常见问题（拦截参考）

以下问题会导致用例被 Phase 02 **直接拦截**，不通过则退回 Phase 01 修正，Phase 02 不执行任何修复。

### 1. Step name 包含非法字符

`name` 字段仅允许：中文、A-Z a-z 0-9、`-` `_` `,` `;` `:` `.` `/` `(` `)` `（` `）` 及空格；长度 1–128；不能为空。

**非法字符**：`[` `]` `|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"`

**拦截**：`name` 含上述非法字符 → 拒收，退回 Phase 01。

### 2. Bare `- uses:` steps 缺少 `name:`

每个 step 必须有 `name`，且 `run` 与 `uses` 不可同时存在。

```yaml
# 拒收示例
- name: (TC-000) checkout source
- uses: checkout
```

**拦截**：`- uses:` 前无同级 `- name:` → 拒收，退回 Phase 01。

### 3. `if:` 表达式必须使用 `${{ }}`

`if:` 中的表达式必须使用 `${{ expr }}`，不能用 `$${ expr }`。

**拦截**：`if:` 含 `$${` → 拒收，退回 Phase 01。

### 4. Job steps 数量限制（≤ 16）

每个 job 的 steps 不能超过 16 条。

**拦截**：任意 job steps > 16 → 拒收，退回 Phase 01。

### 5. `on.push` / `merge_requests` 的 `paths` 与 `paths-ignore` 互斥

两者同时存在时校验不通过。

**拦截**：`paths` 与 `paths-ignore` 共存 → 拒收，退回 Phase 01。

### 6. `if:` 中的裸关键字（不含 `${{ }}`）

| 拒收写法 | 应有写法 |
|---------|---------|
| `if: always` | `if: ${{ always() }}` |
| `if: success()` | `if: ${{ success() }}` |
| `if: failure()` | `if: ${{ failure() }}` |
| `if: cancelled()` | `if: ${{ cancelled() }}` |

**拦截**：`if:` 含裸关键字未包裹 `${{ }}` → 拒收，退回 Phase 01。

### 7. `defaults.run` 下不能包含 `name`

`defaults.run` 仅支持 `shell:` 和 `working-directory:`。

**拦截**：`defaults.run` 含 `name:` → 拒收，退回 Phase 01。

### 8. `vars` 上下文不被 GitCode 支持

引用 `vars.XXX` 会导致"不支持的关键字"错误。

**拦截**：`if:` 或其他字段含 `vars.` → 拒收，退回 Phase 01。

### 9. `workflow_call.inputs` / `secrets` key 命名规则

key 仅允许：大小写英文字母、数字、`_`（下划线），不支持连字符。

**拦截**：key 含 `-` → 拒收，退回 Phase 01。

### 10. `permissions` 范围限制

GitCode 支持的范围：`repository`、`pr`、`issue`、`note`、`project`。

**拦截**：含 `hook`、`actions`、`checks`、`contents`、`deployments`、`packages` 等不支持范围 → 拒收，退回 Phase 01。

### 11. 顶层 `post:` 块

GitCode 不支持顶层 `post:` 属性块（含 `run_always` 和 `steps`）。

**拦截**：含顶层 `post:` → 拒收，退回 Phase 01。

### 12. `runs-on` 格式规则

- `runs-on` **不支持** `${{ }}` 表达式（无论是否用引号包裹）。
- 单字符串值只允许：`default`、`ubuntu-latest`、`euler-latest`。

**拦截**：`runs-on` 含 `${{ }}` 或单字符串非白名单值 → 拒收，退回 Phase 01。

### 13. `env` key 命名规则

job/step 的 `env` 下 key 仅允许：大小写英文字母、数字、`_`，不支持连字符。

**拦截**：`env` key 含 `-` → 拒收，退回 Phase 01。

### 完整检查清单

| # | 检查项 | 触发词 |
|---|--------|--------|
| 1 | Step name 非法字符 | `[` `]` `\|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"` |
| 2 | Bare `uses:` 缺少 `name:` | `- uses:` 前无 `- name:` |
| 3 | `if:` 使用 `$${ }` 而非 `${{ }}` | `$${` |
| 4 | `if:` 表达式缺少 `${{ }}` | 裸 `always` / `success()` 等 |
| 5 | `if:` 中 `always` 未写成 `always()` | `${{ always }}` |
| 6 | `vars` 上下文 | `vars.` |
| 7 | Job steps > 16 | 计数 |
| 8 | `paths` + `paths-ignore` 共存 (push/merge_requests) | `paths-ignore` |
| 9 | `workflow_call.inputs` key 含连字符 | `-` in input key |
| 10 | `permissions` 含不支持的范围 | `hook` 等 |
| 11 | 顶层 `post:` 块 | `post:` at indent 0 |
| 12 | `runs-on` 含 `${{ }}` | `[${{` |
| 13 | `env` key 含连字符 | `-` in env key |
| 14 | `runs-on` 单字符串非白名单值 | `runs-on: ${{` |

### GitCode 平台不支持功能速查

| # | 不支持项 | 替代方案 |
|---|---------|---------|
| 1 | `vars` 上下文 (`vars.XXX`) | 使用 `atomgit` 上下文或删除 |
| 2 | `permissions.hook` 及 GitHub Actions 专有范围 | 仅支持 `repository` `pr` `issue` `note` `project` |
| 3 | 顶层 `post:` 属性块 | 移除，或通过 job 内步骤实现 |
| 4 | `runs-on` 中使用 `${{ }}` 表达式 | 使用硬编码 flow sequence 数组 |
| 5 | `if:` 中裸 `always` 关键字（不写 `()`） | 必须写为 `always()` |
| 6 | `if:` 中 `$${ expr }` 语法 | 必须使用 `${{ expr }}` |
| 7 | `workflow_call.inputs`/`secrets` key 含连字符 | 只能用字母、数字、下划线 |
| 8 | job/step `env` key 含连字符 | 只能用字母、数字、下划线 |
| 9 | `on.push`/`merge_requests` 同时存在 `paths` 和 `paths-ignore` | 保留 `paths`，删除 `paths-ignore` |
| 10 | `runs-on` 单字符串非白名单值 | 使用 flow sequence 数组 |
| 11 | 未包裹 `${{ }}` 的 `if:` 表达式 | 必须加 `${{ }}` 包裹 |
