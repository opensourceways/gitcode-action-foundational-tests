用例 ID:   USE-CTX-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-002
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      使用 github 上下文时报错应提示 atomgit 替代

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 的 run 步骤中引用 ${{ github.ref }}

预期结果:
  YAML 校验或表达式求值阶段报错，提示应使用 atomgit 上下文

验证点:
  - [负向] 不应静默求值为空字符串
  - [非功能] 报错信息中应同时出现 github 与 atomgit 字样

清理:      无

