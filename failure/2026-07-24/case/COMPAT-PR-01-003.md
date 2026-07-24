## 校验失败 · COMPAT-PR-01-003 · PR types 配置后匹配类型不触发与 GitHub 行为差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-NEW-003 | trigger: pull_request
