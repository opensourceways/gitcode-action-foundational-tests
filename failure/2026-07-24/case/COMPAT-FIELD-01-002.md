## 校验失败 · COMPAT-FIELD-01-002 · 含 services 字段的 job 应被报错或警告

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test].services: unknown property

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-021 | trigger: workflow_dispatch
