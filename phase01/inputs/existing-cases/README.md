# inputs/existing-cases/ （建议 · 第一版用例参考）— 已补充 ✅

放 **已有的第一版测试用例列表**。这是 agent 产出新一批用例时的有效补充——避免重复、识别遗漏、继承已有覆盖。

## 已预处理

Excel 已预转换为 **`cases.md`**（Markdown 表，335KB，包含全部 5 个 sheet）。**agent 直接读 `cases.md`**，无需解析 Excel。
Excel 原文件保留于此供你持续更新使用。

## 首次补充（Excel → Markdown）

用例表推荐包含以下列（有就填，没有的列 agent 会标注缺失）：

| 列名 | 说明 | 示例 |
|------|------|------|
| 用例 ID | 已有用例的编号 | `TC-001` |
| 标题 | 用例标题 | `fork PR 不应读取到仓库 secrets` |
| 所属维度 | 功能/安全/稳定性/易用性/兼容性 | `安全` |
| 优先级 | P0/P1/P2 | `P0` |
| 前置条件 | 执行前需满足的状态 | `仓库已配置 secret DEPLOY_TOKEN` |
| 操作步骤 | 执行步骤描述 | `1. fork 仓库 2. 提交含 workflow 的 PR...` |
| 预期结果 | 期望行为 | `workflow 无法读取 DEPLOY_TOKEN` |
| 用例状态 | 已通过 / 未通过 / 未执行 / 已废弃 | `已通过` |
| 备注 | 补充说明 | `需在独立实例上执行` |

> 格式：Excel（`.xlsx` / `.xls`）。
> 命名：随意，建议 `existing-cases-v1.xlsx`。多版本可共存。
> 列名不强求精确匹配——agent 会自适应解析，缺失列在输出中标注。

## 消费方

- **case-writer agent**（最直接消费者）：展开新 intent 为用例前，**先扫已有用例，避免产出等价用例**；若发现已有用例覆盖了新 intent，标注「已有用例覆盖」并给出 ID 关联。
- **orchestrator**：比对已有用例和本轮准入 intent 的覆盖差异——已有用例覆盖了哪些风险项、新 intent 补了哪些盲区。
- **review-gate**：去重时把已有用例纳入考量范围，避免「已有 + 新产 = 双份重复」。

## 刷新时的影响

- 更新 Excel 后：告诉我「重新预处理 existing-cases」，我会重新生成 `cases.md`
- `/phase01-gen` 和 `/phase01-update <run-id> gate` 均会自动读取最新的 `cases.md`

## 已补充 / gitcode-pipeline-test-cases.xlsx / 2026-07-20 / 631 条用例
