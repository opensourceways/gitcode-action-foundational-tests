用例 ID:   COMP-CTX-01-052
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-086~124
母意图:    —
标题:      上下文在条件表达式 if 中注入验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 job 和 step 的 if 条件中使用 atomgit / env / job 上下文
  2. 运行 workflow 验证条件正确解析

预期结果:
  - if 条件中的上下文表达式被正确求值，条件成立时步骤执行，不成立时跳过

验证点:
  - [正向] atomgit.ref 条件正确匹配时步骤执行
  - [正向] env 条件正确匹配时步骤执行
  - [正向] job.status 条件在 job 级 if 可解析

清理:      重置 fixture 仓库
