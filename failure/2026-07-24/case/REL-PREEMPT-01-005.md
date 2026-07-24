## 校验失败 · REL-PREEMPT-01-005 · preemption events 边界值——配置 10 个应正常解析

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L7:C13 — concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_id]

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-005 | trigger: workflow_dispatch
