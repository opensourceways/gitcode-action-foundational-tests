## 校验失败 · REL-RACE-01-048 · 取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[job_b].if: if表达式无法解析 表达式：failure()第1位出现不支持的函数

- 维度: reliability | 优先级: P1
- intent_ref: INTENT-REL-048 | trigger: workflow_dispatch
