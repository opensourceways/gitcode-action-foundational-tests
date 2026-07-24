## 校验失败 · SEC-PERM-01-001 · 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[perm-read].permissions: unknown property

- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-016 | trigger: workflow_dispatch
