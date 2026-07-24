## 校验失败 · COMPAT-FIELD-01-003 · 未知顶层字段不应被静默忽略而应给出警告

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L3:C15 — custom_field: unknown property

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-021 | trigger: workflow_dispatch
