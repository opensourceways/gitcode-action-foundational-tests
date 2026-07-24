用例 ID:   COMPAT-EXPR-01-010
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-009
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    COMPAT-EXPR-01-009
标题:      loose equality null 与空字符串及零的等价性差异

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中使用 eq 表达式比较 null 与空字符串、null 与数字零
  2. 提交并触发 workflow
  3. 观察求值结果是否与 GitHub Actions 一致

预期结果:
  - null 与空字符串、null 与 0 的比较行为应与 GitHub Actions 一致
  - 若存在差异，应明确记录 null 的强制转换规则

验证点:
  - [正向] 表达式求值不报错
  - [非功能] null 比较结果应与 GitHub Actions 行为一致

清理:      fixture
