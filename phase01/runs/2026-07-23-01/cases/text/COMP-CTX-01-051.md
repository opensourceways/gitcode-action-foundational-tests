用例 ID:   COMP-CTX-01-051
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-086~124
母意图:    —
标题:      上下文在 workflow job step 各级注入验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 workflow 级 env 中引用 atomgit 上下文
  2. 在 job 级 env 中引用 env 上下文
  3. 在 step 级 run 中引用 job 上下文和 atomgit 上下文

预期结果:
  - atomgit / env / job 上下文在各级均可正常解析并注入

验证点:
  - [正向] workflow 级 env 可解析 atomgit 属性
  - [正向] job 级 env 可解析 env 属性
  - [正向] step 级 run 可解析 job 和 atomgit 属性

清理:      重置 fixture 仓库
