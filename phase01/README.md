# Phase 01 · 用例设计 Agent Team（可运行骨架）

> 本目录是「场景分析 → 问题分析 → 测试用例产出」阶段的 **可运行、可复现、可增量更新** 的工作区。
> 完整设计手册见根目录 [`../phase01.md`](../phase01.md)；本目录把它落成可跑的 team、流程、命令与模板。

## 这套东西怎么用（3 分钟版）

```
① 补齐输入        → 按 inputs/INPUTS.md 把 5 类输入放进 inputs/ 各子目录
② 打地基（L0）    → /phase01-baseline   产出 Parity Matrix / 风险登记册 / 质量门禁
③ 生成一批用例    → /phase01-gen        新建 runs/<run-id>/，跑完整流程
④ 查看过程数据    → /phase01-status     看 intent 数 / 覆盖度 / 门禁结论 / DoD
⑤ 增量更新        → /phase01-update     重跑某维度 / 补 intent / 局部再展开
⑥ 规范变更重编译  → /phase01-compile    仅由文本用例重新生成 YAML
```

## 目录导航

| 路径 | 是什么 |
|---|---|
| [`process.md`](process.md) | 流程定义：步骤、门禁、run 生命周期、DoD |
| [`rules.md`](rules.md) | 全局规则：命名、优先级、断言纪律、门禁裁决、Oracle 与脱敏红线 |
| [`testing-focus.md`](testing-focus.md) | GitCode Action / workflow 型系统的测试关注点（业界实践总结） |
| [`agents/`](agents/) | 8 个 agent 的完整定义（角色 / 能力 / 方法 / 输入 / 输出 / 护栏） |
| [`inputs/`](inputs/) | 待补充的 5 类输入 + [`INPUTS.md`](inputs/INPUTS.md) 清单总表 |
| [`baseline/`](baseline/) | L0 三份基线产物（人牵头、agent 协助） |
| [`templates/`](templates/) | intent / 文本用例 / 可执行 YAML 模板 |
| [`schema/`](schema/) | 可执行用例 YAML 的校验 schema |
| [`runs/`](runs/) | 按运行批次存档，每次 `/phase01-gen` 生成一个 `<run-id>/` |

## 核心原则（务必先读）

1. **文本用例是 source of truth，YAML 是派生物。** 评审看文本，执行用 YAML；规范变更重编译 YAML 即可。
2. **意图先行。** agent 不直接产用例，先产 test intent，过评审门禁才允许展开——这是控制用例质量与数量的闸门。
3. **没有 L0 基线，不要大规模产用例。** Parity Matrix + 风险登记册 + 质量门禁是优先级与「能否上线」的客观标尺。
4. **四个责任维度**：完备性 / 稳定性 / 安全性 / 易用性。team 按维度组织，不按功能模块。
5. **可复现、可回溯。** 每批次自成一个 run 目录，过程数据（意图库、门禁日志、覆盖度）全部落盘。

## 与第二部分（执行）的边界

本部分只**设计用例**，不执行。交接面是《测试用例契约》——即 `schema/executable-case.schema.yaml` 定义的派生 YAML，随附 L0 三份基线。详见 [`process.md`](process.md) §DoD。
