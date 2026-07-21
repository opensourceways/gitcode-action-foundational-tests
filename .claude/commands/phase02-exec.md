# /phase02-exec — 执行测试用例（检查 + 批量真跑 + 失败归因）

## 用途
Phase 02 核心命令。对 `queue.json` 里通过 schema 校验的用例：**检查其 workflow 是否合规（LLM 检查 fan-out）→ 确定性批量真跑（不合规者自动判 COMPILE_ERROR，不 push）→ 对失败用例做根因初判（LLM 归因 fan-out）**。

> ★ 边界：**编写 workflow 是 Phase 01 的职责**。Phase 02 **不编译、不改写** workflow——只
> 直接用 Phase 01 契约里的 `workflow:` 字段，检查它、执行它。不合规回报 Phase 01 修。

## 架构（两层：Claude 编排 + py 确定性）
```
/phase02-exec (Claude 编排)
  ├─ ① 检查 fan-out：对 workflow 做 GitCode 文档合规检查（yaml-compiler 检查器子 agent）  ← LLM 辅助
  │     + 可选：为可执行断言做夹具绑定 sidecar（compiled/<id>.asserts.json，属执行准备非编写）
  ├─ ② 批量执行：python run_batch.py <run-id>   → 逐条 run_case（preflight 门禁+真跑+teardown） ← 确定性，CI 可直接跑
  └─ ③ 失败归因 fan-out：对 FAIL 用例 → 派 failure-analyst 子 agent 做根因初判              ← LLM 辅助，不改判定
```
**铁律**：pass/fail 只由 `assertion_engine`（②里的 run_case）确定性裁决；①③的 LLM 产物是建议/信号，不改判定（rules.md §1）。

## 参数
- `<phase02-run-id>`：已 schema-check 的批次 id（必需）
- `--only <c1,c2>`：只跑指定用例（可选，增量/重跑）
- `--no-logs`：跳过日志抓取（仅状态型断言，可选）

## 执行步骤

### ① 检查 fan-out（合规检查 + 可选断言绑定）
1. 读 `runs/<run-id>/queue.json`，取每条 case 的 Phase 01 契约 `workflow:`。
2. **合规检查**：`run_batch`/`run_case` 内置的 `preflight_validate`（确定性）已作第一道门禁——列表形式 `on:`、`run:` 冒号、runs-on 格式、非法 step name 等不合规 → 判 `COMPILE_ERROR`，**不 push**、回报 Phase 01。
   - 需要更深的**文档级**检查（preflight 覆盖不到的语义/能力）时，**并行派 yaml-compiler 检查器子 agent**（Task；指令见 `phase02/agents/yaml-compiler/CLAUDE.md`）产出「合规/不合规+GitCode 文档依据」报告。**检查器只检查、不改写**（改写归 Phase 01）。
3. **可选断言绑定**：若契约断言是抽象 rubric，可产出 `compiled/<id>.asserts.json`（rubric→engine kind + 夹具明文，读 `phase02/inputs/fixture-map.md`）。这是**执行前准备**，不碰 workflow，不算越界。缺 sidecar 时 run_case 退化为状态型断言。

### ② 批量执行（确定性）
```
python phase02/scripts/run_batch.py <run-id> [--only ..] [--no-logs]
```
- 逐条：`preflight` 门禁 → push → 触发 → 采集 → §11 判定 → **teardown 删除本次 push 的 workflow 文件**（防污染）。
- `state.json`/`summary.json` **每条增量更新**（故 `/phase02-status` 可中途查看）。
- 不合规（列表形式 on: 等）→ `COMPILE_ERROR`，不 push；契约无 workflow → `NOT_CONFIGURED`。

### ③ 失败归因 fan-out（LLM 辅助，不改判定）
1. 读 `summary.json`，筛出 `verdict=FAIL` 的用例。
2. 对每条 FAIL，**并行派 failure-analyst 子 agent**（Task；指令见 `phase02/agents/failure-analyst/CLAUDE.md`）：读日志/断言详情 + Phase01 文本用例 + GitCode 文档 → 归因「产品缺陷 / 用例问题 / 环境问题 / 文档缺口」，写入 `runs/<run-id>/results/<case-id>.analysis.md`。
3. **立场**：以 GitCode 文档为准绳，文档承诺没做到 = 产品缺陷；别拿 GitHub 当标准（见 failure-analyst 立场原则）。

### 收尾
- 汇报本批：内部判定分布 + COMPILE_ERROR（回报 Phase 01）+ FAIL 归因摘要。提示 `/phase02-report` 出正式报告。

## 输出
- `runs/<run-id>/results/<case-id>.json`+`.md`（逐条）· `.analysis.md`（FAIL 归因）
- `runs/<run-id>/summary.json` · `state.json`（供 status）

## 示例
```
/phase02-exec 2026-07-21-10                          # 检查 + 全量真跑 + 归因
/phase02-exec 2026-07-21-10 --only SEC-MASK-03-001   # 只重跑一条
```
