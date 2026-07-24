## 校验失败 · COMPAT-PERM-01-003 · permissions 命名差异——GitHub contents 权限项应报错

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L4:C13 — permissions.contents: unknown property

- 维度: compatibility | 优先级: P0
- intent_ref: INTENT-COMPAT-030 | trigger: workflow_dispatch
