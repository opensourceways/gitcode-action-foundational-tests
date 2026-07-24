用例 ID:   COMP-CTX-01-053
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-086~124
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      上下文在 Action 插件参数中注入验证

前置条件:
  - 仓库已启用 AtomGit Action
  - 存在可引用的官方 Action

操作步骤:
  1. 在 uses 步骤的 with 参数中使用 atomgit 和 env 上下文
  2. 运行 workflow 验证 Action 接收参数正确

预期结果:
  - Action 的 with 参数中可正常解析 atomgit / env / secrets 上下文

验证点:
  - [正向] with 参数中的上下文表达式被正确替换并传入 Action

清理:      重置 fixture 仓库
