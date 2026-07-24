用例 ID:   USE-EXPR-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-024
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      调用未知函数时报错应提示函数名错误与修正方向

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 if 条件中使用 ${{ unknownFunc() }}

预期结果:
  报错指出未知函数，并建议检查函数名拼写

验证点:
  - [负向] 不应静默通过
  - [非功能] 报错中是否包含 unknownFunc 或未知函数字样

清理:      无

