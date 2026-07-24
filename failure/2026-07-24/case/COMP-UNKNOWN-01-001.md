## 校验失败 · COMP-UNKNOWN-01-001 · 包含未知顶层字段的 workflow 触发 YAML 校验失败

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L1:C16 — unknown_field: unknown property

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-002 | trigger: workflow_dispatch
