用例 ID:   REL-MATRIX-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-007
标题:      strategy.fail-fast=true 时矩阵 1 实例失败其余被取消

前置条件: 矩阵 6 实例，1 个必然失败，fail-fast=true
操作步骤:
  1. 触发 matrix workflow（含 1 个 exit 1）
  2. 验证其余未完成实例在 30s 内被 cancelled
  3. 验证已完成 job 状态不受影响

预期结果: 失败后其余实例被取消；已完成的保留原状态
验证点:
  - [正向] 其余实例状态 cancelled
  - [正向] 已完成的保留
清理:      none
