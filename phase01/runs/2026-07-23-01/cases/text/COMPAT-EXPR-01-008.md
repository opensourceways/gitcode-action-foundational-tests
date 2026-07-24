用例 ID:   COMPAT-EXPR-01-008
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-008
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      toJson 表达式输出格式差异（pretty-print vs compact）

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中定义一个对象或数组
  2. 使用 toJson 表达式函数将其序列化并输出到日志
  3. 观察输出格式是否包含换行与缩进

预期结果:
  - toJson 输出应为合法 JSON
  - 若 GitCode 与 GitHub 行为一致，应输出 compact 单行 JSON
  - 若存在差异，应明确记录 pretty-print 与 compact 的行为分界

验证点:
  - [正向] toJson 输出合法 JSON
  - [非功能] 输出格式应与 GitHub Actions 行为一致或文档中明确说明差异

清理:      fixture
