用例 ID:   REL-MATRIX-02-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-008
标题:      strategy.max-parallel=3 时，6 实例矩阵的并发峰值不超过 3

前置条件:
  - 矩阵有 6 个实例，每个 step 有 sleep 30
  - max-parallel=3

操作步骤:
  1. 触发含 6 实例、max-parallel=3 的矩阵 workflow
  2. 观察任意时刻 in_progress 的矩阵 job 数是否 ≤ 3
  3. 验证 6 个 job 全部到达 completed 终态

预期结果:
  - 任意快照时刻 in_progress 矩阵 job 数 ≤ 3
  - 6 个 job 全部完成
  - 无 job 因 slot 不足而永久卡在 queued

验证点:
  - [正向] 同时 in_progress 矩阵 job 数 ≤ 3
  - [正向] 6 个 job 全部到达 completed
  - [负向] 无 job 永久卡在 queued

清理:      fixture
