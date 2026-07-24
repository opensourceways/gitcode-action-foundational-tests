## 校验失败 · REL-PREEMPT-01-006 · preemption events 越界值——配置 11 个应被拒绝

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (2 条):
  - [Error] L7:C13 — concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_id]
  - [Error] L7:C13 — concurrency.preemption.events: 列表长度必须在0到10之间

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-006 | trigger: workflow_dispatch
