用例 ID:   REL-MATRIX-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-007
标题:      strategy.fail-fast=true 时，矩阵中 1 个 job 失败应立即取消其余未完成实例

前置条件:
  - 矩阵有 6 个实例
  - 其中 1 个布置必然失败（exit 1），其余有 sleep 120

操作步骤:
  1. 触发含有 6 实例的矩阵 workflow
  2. 观察首个 job 失败后，其余未完成实例的取消行为
  3. 验证已完成的实例状态不受影响

预期结果:
  - 首个 job 失败后其余未完成 job 在 30s 内全部转为 cancelled
  - 已完成的 job 状态不受影响
  - 无 job 卡死在 in_progress 超过 60s

验证点:
  - [正向] 其余未完成 job 30s 内 cancelled
  - [正向] 已完成 job 状态不变
  - [负向] 无 job stuck in_progress > 60s

清理:      fixture
