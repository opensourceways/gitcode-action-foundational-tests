## 校验失败 · USE-UNKN-01-001 · 未知字段如 run-name 不应被静默忽略而应给出警告或错误

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L1:C11 — run-name: unknown property

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-023 | trigger: workflow_dispatch
