用例 ID:   COMP-BOUND-01-086
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-276~328
母意图:    —
标题:      矩阵构建 include exclude 与单值边界验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 matrix include 和 exclude 的 strategy
  2. 验证矩阵展开和排除行为

预期结果:
  - matrix 支持单变量和多变量，include 添加额外组合，exclude 排除特定组合，单值变量正确展开

验证点:
  - [正向] include 添加的组合在 step 中可访问
  - [正向] exclude 排除的组合不产生 job 实例
  - [正向] 单值变量正确展开

清理:      重置 fixture 仓库
