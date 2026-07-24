用例 ID:   COMP-JOB-01-067
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-264~288
母意图:    —
标题:      job 可选字段 env if timeout-minutes needs 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 env / if / timeout-minutes / needs 的 job
  2. 验证各字段生效

预期结果:
  - job 级 env 对该 job 所有 step 可见，if 条件正确控制 job 是否执行，timeout-minutes 限制执行时长，needs 正确建立依赖

验证点:
  - [正向] job env 在 step 中可访问
  - [正向] needs 依赖 job 先执行
  - [正向] timeout-minutes 字段被接受

清理:      重置 fixture 仓库
