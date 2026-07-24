## 校验失败 · COMP-WFLOW-01-065 · workflow post 后处理阶段字段验证

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L14:C5 — post.steps: unknown property
  - [Error] L12:C15 — post.run_always: unknown property

- 维度: completeness | 优先级: P1
- intent_ref: KEEP-TC-366~401 | trigger: workflow_dispatch
