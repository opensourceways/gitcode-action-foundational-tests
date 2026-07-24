## 校验失败 · USE-YAML-01-001 · 缺少必填字段 on 时报错应指出具体字段名与位置

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — on: 值不能为空

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-022 | trigger: workflow_dispatch
