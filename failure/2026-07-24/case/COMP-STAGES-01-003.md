## 校验失败 · COMP-STAGES-01-003 · post.run_always true 时 workflow 失败仍执行 post

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L14:C5 — post.steps: unknown property
  - [Error] L12:C15 — post.run_always: unknown property

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-007 | trigger: workflow_dispatch
