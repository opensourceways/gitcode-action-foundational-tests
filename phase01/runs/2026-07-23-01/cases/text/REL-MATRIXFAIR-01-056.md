用例 ID:   REL-MATRIXFAIR-01-056
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-056
母意图:    —
标题:      矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发 20 实例 matrix 配 max-parallel=4，每实例 sleep 30s

预期结果:
  - 20 实例 100% 完成
  - 最大 queued 延迟≤3×最小延迟
  - 总耗时≈3min

验证点:
  - [正向] 20 实例全部完成
  - [非功能] 最大/最小 queued 延迟比≤3
  - [负向] 无实例被无限饿死

清理:      无需特殊清理
