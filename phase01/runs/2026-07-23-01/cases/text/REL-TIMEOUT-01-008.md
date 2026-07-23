用例 ID:   REL-TIMEOUT-01-008
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-008
母意图:    —
标题:      job timeout 越界触发——361 分钟应在 360 分钟被强制终止

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21660

预期结果:
  - job 在 360±2 分钟时被终止
  - 状态为 failure
  - 日志含超时信息

验证点:
  - [正向] job 状态=failure
  - [正向] 日志含 timeout 或 超时
  - [负向] 不应运行超过 365 分钟

清理:      无需特殊清理
