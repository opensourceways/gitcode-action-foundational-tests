## 校验失败 · COMP-SCHEDULE-01-002 · 非默认分支的 schedule workflow 不应触发

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L3:C13 — on.schedule[0].cron: 不是可识别的cron表达式

- 维度: completeness | 优先级: P1
- intent_ref: INTENT-COMP-005 | trigger: schedule
