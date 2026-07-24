## 校验失败 · COMPAT-EXPR-01-014 · always() 带括号与不带括号的兼容性差异

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[test-always-paren].steps[1].if: if表达式无法解析 表达式：always第1位出现不支持的关键字

- 维度: compatibility | 优先级: P1
- intent_ref: INTENT-COMPAT-004 | trigger: workflow_dispatch
