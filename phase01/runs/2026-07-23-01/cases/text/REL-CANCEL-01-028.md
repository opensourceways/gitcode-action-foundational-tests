用例 ID:   REL-CANCEL-01-028
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-028
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      手动取消 workflow——运行中取消时 always() cleanup step 仍应执行

前置条件:
  - 仓库存在一条正在运行的 workflow

操作步骤:
  1. 手动取消该 workflow

预期结果:
  - 非 always step 被终止
  - if: ${{ always() }} 的 cleanup step 被执行
  - workflow 最终状态=cancelled

验证点:
  - [正向] 非 always step 被终止
  - [正向] cleanup step 日志存在且 completed
  - [正向] workflow 状态=cancelled

清理:      无需特殊清理
