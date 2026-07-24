用例 ID:   COMP-BOUND-01-084
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-514~559
母意图:    —
标题:      路径与分支过滤组合及否定模式边界验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 配置 push 的 branches 和 paths 组合过滤，使用否定模式
  2. 验证仅肯定模式触发，否定模式需与肯定模式组合

预期结果:
  - branches 和 paths 同时存在时为 AND 关系，否定模式 ! 需与肯定模式组合，仅否定模式不触发

验证点:
  - [正向] branches + paths 组合过滤生效
  - [负向] 仅否定模式时不触发 workflow
  - [正向] 否定模式与肯定模式组合生效

清理:      重置 fixture 仓库
