用例 ID:   REL-TIMEOUT-01-009
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-009
母意图:    —
标题:      自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发 timeout-minutes=1 的 workflow，step 执行 sleep 120

预期结果:
  - job 在 60±10 秒时被终止
  - 状态为 failure
  - 日志含超时信息

验证点:
  - [正向] job 状态=failure
  - [正向] 实际运行时长 60±10 秒

清理:      无需特殊清理
