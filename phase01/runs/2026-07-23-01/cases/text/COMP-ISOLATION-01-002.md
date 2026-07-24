用例 ID:   COMP-ISOLATION-01-002
维度标签:   [completeness, reliability, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-011
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      环境变量不跨 job 泄漏

前置条件:
  - workflow 含两个串行 jobs

操作步骤:
  1. job 1 设置环境变量
  2. job 2 检查该环境变量

预期结果:
  - job 2 不应看到 job 1 设置的环境变量

验证点:
  - [负向] job 2 中环境变量值为空或未设置

清理:      none
