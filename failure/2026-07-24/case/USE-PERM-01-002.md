## 校验失败 · USE-PERM-01-002 · 使用 GitHub 权限域命名时报错应给出 GitCode 对照表

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L2:C13 — permissions.contents: unknown property

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-005 | trigger: workflow_dispatch
