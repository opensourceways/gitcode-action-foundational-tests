## 校验失败 · USE-TYPE-01-002 · 使用 GitHub types 命名 opened/synchronize 时应给出可理解提示

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close, merge, open, reopen, update]

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-009 | trigger: pull_request
