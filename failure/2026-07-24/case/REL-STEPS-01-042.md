## 校验失败 · REL-STEPS-01-042 · 超多 step——单 job 内 50 个 step 应全部串行执行无丢失

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test].steps: 列表长度必须在0到16之间

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-042 | trigger: workflow_dispatch
