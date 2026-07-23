用例 ID:   REL-TIMEOUT-01-007
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-007
母意图:    —
标题:      job timeout 边界值——359 分钟运行应在 360 分钟边界前完成

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21540

预期结果:
  - job 在 359 分钟前成功完成
  - 状态为 success

验证点:
  - [正向] job 状态=success
  - [负向] 不应在 358 分钟前被强制终止

清理:      无需特殊清理
