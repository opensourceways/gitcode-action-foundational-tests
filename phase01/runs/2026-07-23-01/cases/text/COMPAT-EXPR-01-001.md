```
用例 ID:   COMPAT-EXPR-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-004
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      success 关键字在条件表达式中的可用性

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个 workflow，其中包含多个 step
  2. 在 step 执行过程中，尝试通过表达式获取当前的成功状态信息
  3. 观察平台对 success 关键字的解析与返回值

预期结果:
  - 若平台支持 success 关键字，则可在适当上下文中获取到状态值
  - 若不支持，应有明确的表达式解析行为（如视为字符串或报错）

验证点:
  - [正向] 表达式被正确解析，日志中输出预期值
  - [负向] 若平台拒绝该关键字，应记录兼容性差异

清理:      重置 fixture 仓库
```
