用例 ID:   USE-STAT-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-004
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      使用 success() 带括号时报错应提示 GitCode 括号差异

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 step 中使用 if: ${{ success() }}

预期结果:
  YAML 校验或表达式求值报错，提示 GitCode 状态函数不带括号

验证点:
  - [负向] 不应静默通过校验
  - [非功能] 报错中应包含括号差异提示

清理:      无

