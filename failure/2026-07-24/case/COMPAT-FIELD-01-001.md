## 校验失败 · COMPAT-FIELD-01-001 · 含 run-name 字段的 workflow 应被报错或警告

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L1:C11 — run-name: unknown property

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-021 | trigger: workflow_dispatch
