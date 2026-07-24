## 校验失败 · USE-EXPR-01-002 · 调用未知函数时报错应提示函数名错误与修正方向

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[bad].steps[0].if: if表达式无法解析 表达式：unknownFunc()第1位出现不支持的函数

- 维度: usability | 优先级: P1
- intent_ref: INTENT-USE-024 | trigger: workflow_dispatch
