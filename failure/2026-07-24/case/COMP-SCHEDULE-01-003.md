## 校验失败 · COMP-SCHEDULE-01-003 · cron 间隔短于 5 分钟时被拒绝或降级

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L3:C13 — on.schedule[0].cron: 不是可识别的cron表达式

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-005 | trigger: schedule
