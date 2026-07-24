## 校验失败 · COMPAT-ENVIRON-01-001 · 含 environment 字段的 job 应被报错或警告

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test].environment: unknown property

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-023 | trigger: workflow_dispatch
