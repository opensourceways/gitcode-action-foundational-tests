## 校验失败 · COMP-EXPR-01-058 · 表达式运算符与优先级边界行为

**判定结果**: INVALID

**根因**: 平台 schema 校验不通过
**诊断信息** (1 条):
  - [Error] L0:C0 — jobs[verify].steps[2].if: if表达式无法解析 {0}

- 维度: completeness | 优先级: P1
- intent_ref: KEEP-TC-160~175 | trigger: workflow_dispatch
