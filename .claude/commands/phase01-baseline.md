---
description: 产出/刷新 L0 三份验收基线（Parity Matrix / 风险登记册 / 质量门禁）
---

你正在执行 GitCode Action 测试用例设计流程的 **L0 基线**步骤。这是 team 启动的地基——没有 L0，后续会产出海量低价值用例。

## 先读
- `phase01/process.md` §1（L0 基线流程）
- `phase01/rules.md`（命名/优先级/Oracle/脱敏）
- `phase01/testing-focus.md`（关注点骨架）
- `phase01/inputs/INPUTS.md`，并检查 `phase01/inputs/` 各子目录是否已补充资料

## 执行
1. **检查输入**：若 `inputs/gitcode-spec/`、`inputs/github-reference/` 为空，提醒用户补充（可继续，但产物会标注缺口）。
2. **起手冒烟**：若 `inputs/workflow-samples/` 有样本，梳理 3~5 个真实 workflow 应覆盖的能力，作为 Parity Matrix 左列种子。
3. 用 Task 工具拉起 **spec-analyst**（读 `agents/spec-analyst/CLAUDE.md`）产出结构化能力清单，回流 `baseline/parity-matrix.md` 左列。
4. 与用户协作填充/刷新三份基线：
   - `baseline/parity-matrix.md` — 能力 × 支持状态
   - `baseline/risk-register.md` — 风险 × 影响 × 概率 × 优先级 × blocker
   - `baseline/quality-gate.md` — 分维度阈值 + blocker 规则
5. **门禁**：三份非空且经用户评审后，提示可运行 `/phase01-gen`。

## 参数
`$ARGUMENTS` 可为 `refresh`（在既有基线上增量刷新）或空（首次建立）。

## 产出
更新 `phase01/baseline/` 三份文件。**STOP** 把三份基线摊给用户确认，不要自动进入生成阶段。
