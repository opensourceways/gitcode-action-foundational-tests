用例 ID:   SEC-INJ-01-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-013
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      表达式求值必须防止双重模板渲染（二次求值）

前置条件:
  - 仓库支持表达式求值

操作步骤:
  1. 提交一个 workflow，在输入中包含模板语法字符（如 {{ 1 + 1 }}）
  2. 触发 workflow 并查看运行日志

预期结果:
  - 外层 ${{ }} 求值结果中的模板语法字符应被转义
  - 不再触发内层模板引擎求值

验证点:
  - [负向] 含模板语法的外部输入绝不应在内层 Action 中被二次求值
  - [非功能] 二次求值若无法避免，应至少被沙箱化

清理:      重置 fixture 仓库
