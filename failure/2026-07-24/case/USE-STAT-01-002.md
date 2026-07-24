## 校验失败 · USE-STAT-01-002 · 使用 success() 带括号时报错应提示 GitCode 括号差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[bad-stat].steps[0].if: if表达式无法解析 表达式：success()第1位出现不支持的函数

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-004 | trigger: workflow_dispatch
