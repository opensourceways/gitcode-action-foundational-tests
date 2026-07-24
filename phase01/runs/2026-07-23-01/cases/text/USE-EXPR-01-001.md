用例 ID:   USE-EXPR-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-024
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      引用不存在的上下文属性时报错应包含原始表达式与错误类型

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 run 步骤中使用 ${{ atomgit.nonexistent_property }}

预期结果:
  报错包含原始表达式字符串和错误类型说明（undefined property / unknown context）

验证点:
  - [负向] 不应静默求值为空字符串
  - [非功能] 报错中是否包含原始表达式和错误位置

清理:      无

