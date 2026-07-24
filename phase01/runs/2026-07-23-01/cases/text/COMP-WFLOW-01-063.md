用例 ID:   COMP-WFLOW-01-063
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-289~293
母意图:    —
标题:      workflow concurrency 并发控制字段验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 workflow 级定义 concurrency 配置
  2. 验证 max / exceed-action / preemption.events 字段

预期结果:
  - concurrency 配置被平台接受，max >= 1，exceed-action 为 QUEUE 或 IGNORE，preemption.events 仅允许 mr_id

验证点:
  - [正向] 合法 concurrency 配置通过校验
  - [负向] max 小于 1 被拒绝
  - [负向] preemption.events 含非 mr_id 被拒绝

清理:      重置 fixture 仓库
