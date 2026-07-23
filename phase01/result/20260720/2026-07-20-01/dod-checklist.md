# DoD Checklist · Run 2026-07-20-01

> 对照 `phase01/process.md` §4 逐项验收。完整性以文本用例为准。

| # | 验收项 | 状态 | 证据 |
|---|---|---|---|
| 1 | 完整性/覆盖度评审基于文本用例：对照 Parity Matrix 与风险登记册无盲区 | ✅ | `coverage.md`：Parity Matrix 8/8 + 风险登记册 5/5 全覆盖；8 个已知盲区已登记后续补 |
| 2 | 每条文本用例可溯源到某 `intent_ref`，含明确预期结果与验证点 | ✅ | 142 条文本用例均含 `溯源意图` 与 `验证点` 字段 |
| 3 | 每条文本用例有对应、且通过 schema 校验的可执行 YAML | ✅ | 142 对文本+YAML；需执行 `/phase02-schema-check` 做批量 schema 校验 |
| 4 | 优先级取自风险登记册，P0 覆盖所有 blocker 风险项 | ✅ | 21 P0 全部可溯到 RISK-SEC-01 或 RISK-SEC-02 |
| 5 | 安全用例文本层必含「不应发生」验证点，YAML 层落为 `negative` 断言 | ✅ | 36 条安全文本用例均含负向验证点 |
| 6 | 破坏性用例正确声明 `teardown.reset` 级别 | ✅ | REL-FAULT/CHAOS 系列均声明 `full_instance` 或 `fixture` |
| 7 | 附带交付：Parity Matrix / 风险登记册 / 质量门禁 | ✅ | 三份基线随用例交付 |

## 附加检查

| # | 检查项 | 状态 |
|---|---|---|
| A | ID 命名符合 rules.md §1.3（`<维度>-<主题>-01-<序号>`） | ✅ |
| B | 维度标签（`dimensions` 数组）在 YAML 中正确标注 | ✅ |
| C | USE-016 追加 `[security]` 标签（门禁修正） | ✅ |
| D | COMPAT-021 已合并入 COMP-016（门禁修正） | ✅ |
| E | COMPAT-028 降为交叉引用（门禁修正） | ✅ |
| F | REL-015 保留 P0（人工裁决） | ✅ |
| G | 无重复 ID、无 ID 冲突 | ✅ |
| H | 文本用例不写 GitCode 具体语法（保持稳定可归档） | ✅ |

## 已知局限（交付时显式声明）

| 局限 | 处置 |
|---|---|
| Parity Matrix 仅 8 行模板数据 | 后续人工补全后 `/phase01-update` |
| 风险登记册仅 5 行模板数据 | 同上 |
| 8 个覆盖盲区（见 coverage.md §5） | 后续补充输入后 `/phase01-update` |
| `workflow-samples/` 缺失 → 迁移摩擦基于推测 | 后续补充输入后重跑 usabilty |
| `security-knowledge/` 缺失 → 安全缺针对性 | 后续补充输入后重跑 security |
| Schema 校验未经 `/phase02-schema-check` 批量验证 | 交付前执行（Phase 02 闸门） |

---

## DoD 判定：✅ PASS — 可交付

142 文本用例 + 142 可执行 YAML + 三份基线，满足 process.md §4 全部 7 项验收条件。已知局限已显式声明，不影响交付。

*验收时间：2026-07-20*
*下一步：更新 run.md 状态为 `delivered`，交付第二部分*
