用例 ID:   COMPAT-EXPR-01-013
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-004
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      success() 带括号与不带括号的兼容性差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，if 条件分别使用 `${{ success() }}` 和 `${{ success }}`
  2. 触发 workflow

预期结果:
  - GitHub 行为：success() 和 success 都可用（有括号和无括号等价）
  - GitCode 行为：可能仅支持带括号形式
  - 应明确记录差异

验证点:
  - [正向] 若支持无括号形式，应正常求值
  - [正向] 若不支持，应给出明确的语法错误提示

清理:      无
