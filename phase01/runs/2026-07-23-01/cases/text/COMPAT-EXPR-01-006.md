```
用例 ID:   COMPAT-EXPR-01-006
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-007
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      hashFiles 表达式无匹配路径边界

前置条件:
  - 仓库已启用 GitCode Action
  - 仓库中不存在名为 nonexistent-pattern.xyz 的文件

操作步骤:
  1. 提交一个 workflow，在 step 中使用 hashFiles 匹配一个不存在的文件模式
  2. 例如 hashFiles('**/nonexistent-pattern.xyz')
  3. 手动触发并观察输出结果

预期结果:
  - hashFiles 对无匹配路径返回空字符串或确定的默认值
  - 验证无匹配时的行为与 GitHub Actions 是否一致

验证点:
  - [正向] 无匹配时返回空字符串
  - [负向] 无匹配时不应抛出异常导致 step 失败
  - [正向] 日志中可观察到空结果或占位符

清理:      重置 fixture 仓库
```
