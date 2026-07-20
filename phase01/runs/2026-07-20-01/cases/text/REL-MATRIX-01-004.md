用例 ID:   REL-MATRIX-01-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-008
标题:      strategy.max-parallel=3 时 6 实例并发峰值不超过 3

前置条件: 矩阵 6 实例，max-parallel=3
操作步骤:
  1. 触发 matrix workflow
  2. 验证任意时刻 in_progress <= 3
  3. 验证 6 个 job 全部到达 completed

预期结果: 并发峰值 <= 3；全部完成无卡死
验证点:
  - [正向] in_progress <= 3
  - [正向] 6 个全部完成
清理:      none
