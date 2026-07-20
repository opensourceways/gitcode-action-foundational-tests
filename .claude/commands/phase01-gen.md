---
description: 新建一个 run 批次，跑完整用例设计流程（发散→门禁→展开→DoD）
---

你正在执行 GitCode Action 测试用例设计的**完整生成**。严格按 `phase01/process.md` §2 的阶段与门禁推进。

## 前置检查
- `phase01/baseline/` 三份基线非空（否则先 `/phase01-baseline`）。
- `phase01/inputs/` 关键输入已补充（缺则相关维度会退化，在产物中标注）。

## 参数
`$ARGUMENTS`：可选，限定维度，如 `security compat` 只跑安全与兼容性；空=全维度（spec/compat/security/reliability/usability）。

## 执行步骤

### 0. 新建 run
在 `phase01/runs/` 下按 `YYYY-MM-DD-NN` 新建目录，写 `run.md`：记录触发参数、输入快照（inputs/ 与 baseline/ 的时间戳/版本）、时间线、状态=`open`。

### 1. 阶段A — 发散（并行）
用 Task 工具**并行**拉起选定维度的 agent（各读 `phase01/agents/<name>/CLAUDE.md`），传入：run 目录、L0 基线路径、`rules.md`、`testing-focus.md`、对应 `inputs/`。各 agent 把 intent 写到 `runs/<id>/intents/<dim>.md`。完成后汇总进 `intent-library.md`。

### 2. 评审门禁 — 收敛（STOP①）
用 Task 拉起 **review-gate** + **orchestrator**：去重、按风险登记册定优先级、对照 Parity Matrix 查覆盖盲区，写 `gate-log.md`，回标 `intent-library.md`（准入/打回）。
**STOP**：把「准入意图清单 + 覆盖盲区清单」摊给用户，等确认（可增补专家 intent、否决低价值项）。状态→`gated`。

### 3. 阶段B — 展开+编译
用 Task 拉起 **case-writer**：准入 intent → `cases/text/<ID>.md`（文本用例，归档主体）→ 编译 `cases/yaml/<ID>.yaml`（过 `schema/` 校验）。

### 4. 验收（STOP②）
生成 `coverage.md`（对照 Parity Matrix + 风险登记册）与 `dod-checklist.md`（按 `process.md` §4）。
**STOP**：DoD 全绿、无覆盖盲区后，状态→`delivered`，提示可交付第二部分。

## 纪律
- 意图先行：不得跳过门禁直接产用例。
- 每步更新 `run.md` 时间线。
- 遵守 `rules.md` 全部条款（尤其脱敏红线与溯源链）。
