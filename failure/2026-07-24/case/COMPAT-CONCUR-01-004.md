## 校验失败 · COMPAT-CONCUR-01-004 · concurrency preemption events 越界时行为差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (3 条):
  - [Error] L0:C0 — concurrency.exceed-action: 值不能为空
  - [Error] L0:C0 — concurrency.max: 值不能小于1
  - [Error] L7:C13 — concurrency.preemption.events: 列表中存在非法值:[11] 允许值:[mr_id]

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-NEW-005 | trigger: workflow_dispatch
