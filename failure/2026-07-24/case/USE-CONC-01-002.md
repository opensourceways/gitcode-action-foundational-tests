## 校验失败 · USE-CONC-01-002 · concurrency.max 配置 -1 时报错应提示有效范围

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L2:C8 — concurrency.max: 值不能小于1

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-027 | trigger: workflow_dispatch
