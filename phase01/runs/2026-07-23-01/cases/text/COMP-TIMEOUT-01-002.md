用例 ID:   COMP-TIMEOUT-01-002
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-008
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      超时的 job 被强制终止并标记为 failure

前置条件:
  - workflow 声明 timeout-minutes: 1

操作步骤:
  1. 触发 workflow，其中 step 睡眠超过 1 分钟
  2. 观察 job 是否在 1 分钟后被强制终止

预期结果:
  - job 在 1 分钟后被强制终止
  - 运行状态标记为 failure
  - 已运行 step 的日志保留

验证点:
  - [负向] 运行状态为 failure
  - [正向] 超时前已完成的 step 日志完整保留

清理:      none
