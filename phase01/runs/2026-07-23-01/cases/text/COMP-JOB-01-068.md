用例 ID:   COMP-JOB-01-068
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-276~278
母意图:    —
标题:      job strategy 矩阵与 continue-on-error 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 strategy.matrix 和 continue-on-error 的 job
  2. 验证矩阵展开和容错行为

预期结果:
  - strategy.matrix 正确展开多实例，continue-on-error true 时 job 失败不终止 workflow

验证点:
  - [正向] 矩阵变量在 step 中可访问
  - [正向] continue-on-error true 被接受
  - [正向] fail-fast 字段被接受

清理:      重置 fixture 仓库
