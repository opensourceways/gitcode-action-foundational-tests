用例 ID:   COMP-WFLOW-01-065
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-366~401
母意图:    —
标题:      workflow post 后处理阶段字段验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 post 阶段的 workflow
  2. 验证 run_always 默认 true 和 false 时的行为

预期结果:
  - post 阶段在 workflow 结束后执行，run_always 为 true 时无论成败都执行，为 false 时仅成功时执行

验证点:
  - [正向] post 步骤在成功时执行
  - [正向] run_always true 时失败 workflow 仍执行 post

清理:      重置 fixture 仓库
