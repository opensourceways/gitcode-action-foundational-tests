用例 ID:   COMP-WFLOW-01-062
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-366~401
母意图:    —
标题:      workflow env 与 defaults 字段验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 workflow 级定义 env 和 defaults.run
  2. 在 job 和 step 中验证继承与覆盖

预期结果:
  - workflow 级 env 对所有 job/step 可见，defaults.run.shell 和 working-directory 可被 job/step 覆盖

验证点:
  - [正向] workflow env 在 step 中可访问
  - [正向] defaults shell 被正确继承
  - [正向] step 级 shell 覆盖 defaults

清理:      重置 fixture 仓库
