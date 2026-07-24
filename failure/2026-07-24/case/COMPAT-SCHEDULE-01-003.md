## 校验失败 · COMPAT-SCHEDULE-01-003 · schedule 在非默认分支不触发与 GitHub 差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L3:C13 — on.schedule[0].cron: 不是可识别的cron表达式

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-013 | trigger: schedule
