## 校验失败 · COMP-BOUND-01-085 · cron 表达式格式与位置边界验证

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (3 条):
  - [Error] L3:C13 — on.schedule[0].cron: 不是可识别的cron表达式
  - [Error] L4:C13 — on.schedule[1].cron: 不是可识别的cron表达式
  - [Error] L5:C13 — on.schedule[2].cron: 不是可识别的cron表达式

- 维度: completeness | 优先级: P1
- intent_ref: KEEP-TC-475~512 | trigger: schedule
