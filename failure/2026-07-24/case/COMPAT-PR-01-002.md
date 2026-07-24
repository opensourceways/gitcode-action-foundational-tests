## 校验失败 · COMPAT-PR-01-002 · pull_request types 命名差异 - GitHub 风格 types 应报错

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close, merge, open, reopen, update]

- 维度: compatibility | 优先级: P0
- intent_ref: INTENT-COMPAT-011 | trigger: pull_request
