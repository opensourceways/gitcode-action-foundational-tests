```
用例 ID:   COMPAT-EXPR-01-004
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-006
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      contains 表达式大小写敏感边界

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个 workflow，在 step 中使用 contains 表达式分别检查大小写不同的字符串
  2. 例如检查 contains('Hello World', 'world') 与 contains('Hello World', 'World')
  3. 手动触发并观察输出结果

预期结果:
  - contains 表达式按平台实际实现返回 true 或 false
  - 验证大小写敏感行为与 GitHub Actions 是否一致

验证点:
  - [正向] 大小写匹配时返回 true
  - [正向] 大小写不匹配时返回 false（若平台为大小写敏感）
  - [负向] 结果不应与预期语义矛盾

清理:      重置 fixture 仓库
```
