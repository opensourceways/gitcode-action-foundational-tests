用例 ID:   COMP-STAGES-01-003
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-007
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      post.run_always true 时 workflow 失败仍执行 post

前置条件:
  - workflow 定义 post 阶段且 run_always: true

操作步骤:
  1. 触发 workflow 使主流程 job 失败
  2. 观察 post 阶段是否仍执行

预期结果:
  - 主 workflow 失败
  - post 阶段仍被执行

验证点:
  - [正向] post 阶段步骤日志存在
  - [正向] post 阶段步骤输出出现在运行详情页

清理:      none
