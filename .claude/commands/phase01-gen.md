---
description: 新建一个 run 批次，跑完整用例设计流程（发散→门禁→展开→DoD）
---

你正在执行 GitCode Action 测试用例设计的**完整生成**。严格按 `phase01/process.md` §2 的阶段与门禁推进。

## 前置检查
- `phase01/baseline/` 三份基线非空（否则先 `/phase01-baseline`）。
- `phase01/inputs/` 关键输入已补充（缺则相关维度会退化，在产物中标注）。

## 参数

`$ARGUMENTS`：可选，支持两种形式混用：

1. **限定维度**：如 `security compat` 只跑安全与兼容性；空=全维度（spec/compat/security/reliability/usability）。
2. **`--baseline`**：基准重生成模式。带上此 flag 时，**不复制上轮 delivered run 的用例**，直接对本轮全部准入 intent 从零展开+编译，产出统一格式的新基准全集。
   - 适用场景：格式统一、schema 不兼容升级、新旧用例混杂需刷新、季度基准重建。
   - 可与维度限定混用：`--baseline security` = 仅对 security 维度做基准重生成。

## 执行步骤

### 0. 新建 run
在 `phase01/runs/` 下按 `YYYY-MM-DD-NN` 新建目录，写 `run.md`：记录触发参数（含是否 `--baseline`）、输入快照、时间线、状态=`open`。

### 1. 阶段A — 发散（并行）
用 Task 工具**并行**拉起选定维度的 agent（各读 `phase01/agents/<name>/CLAUDE.md`），传入：run 目录、L0 基线路径、`rules.md`、`testing-focus.md`、对应 `inputs/`。各 agent 把 intent 写到 `runs/<id>/intents/<dim>.md`。完成后汇总进 `intent-library.md`。

### 2. 评审门禁 — 收敛（STOP①）
用 Task 拉起 **review-gate** + **orchestrator**：去重、按风险登记册定优先级、对照 Parity Matrix 查覆盖盲区，写 `gate-log.md`，回标 `intent-library.md`（准入/打回）。
**STOP**：把「准入意图清单 + 覆盖盲区清单」摊给用户，等确认（可增补专家 intent、否决低价值项）。状态→`gated`。

### 3. 阶段B — 展开+编译（分支）

#### 3a. 默认模式（增量 / 基底加速）
`case-writer` 采用**基底加速**（`rules.md` §9b）：
1. 复制最近 `delivered` run 的 `cases/text/` + `cases/yaml/` 到本轮目录。
2. 将准入 intent 与完整基底 diff——已覆盖的不重复生成；未覆盖的标记缺口。
3. 仅对缺口增量生成文本用例 → `cases/text/<ID>.md` + 编译 YAML → `cases/yaml/<ID>.yaml`。
4. `case-manifest.md` = 历史用例 + 新增用例，一份全集清单。

#### 3b. `--baseline` 模式（基准重生成）
`case-writer` **不复制历史用例**，直接对本轮**全部准入 intent** 展开：
1. 跳过「复制上轮用例」步骤，`cases/` 目录从零开始。
2. 每条准入 intent 生成 1-3 条标准 Phase 01 格式用例（text + YAML）。
3. `case-manifest.md` = 本轮全新用例的全集清单（无历史复用记录）。
4. `run.md` 中显式标注触发模式为 `baseline`。

### 4. 验收（STOP②）
生成 `coverage.md`（对照 Parity Matrix + 风险登记册）与 `dod-checklist.md`（按 `process.md` §4）。
**STOP**：DoD 全绿、无覆盖盲区后，状态→`delivered`，提示可交付第二部分。

## 纪律
- 意图先行：不得跳过门禁直接产用例。
- 每步更新 `run.md` 时间线。
- 遵守 `rules.md` 全部条款（尤其脱敏红线与溯源链）。
