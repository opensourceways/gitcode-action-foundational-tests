## 校验失败 · SEC-ENV-01-002 · 环境级 secret 审批前 workflow 不可读取

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[env-secret-denied].environment: unknown property

- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-027 | trigger: workflow_dispatch
