用例 ID:   USE-ENV-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-003
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      引用 GITHUB_SHA 时日志应给出环境变量映射提示

前置条件:
  - workflow 在 GitCode Runner 上执行

操作步骤:
  1. 在 run 步骤中输出 $GITHUB_SHA

预期结果:
  日志中应出现关于 GITHUB 变量不存在或建议使用 ATOMGIT 的提示

验证点:
  - [负向] 不应静默输出空值后继续
  - [非功能] 日志中是否出现 ATOMGIT 前缀的环境变量指引

清理:      无

