用例 ID:   REL-PRESSURE-01-055
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-055
母意图:    —
标题:      并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率

前置条件:
  - 仓库具备 workflow 触发权限

操作步骤:
  1. 在 10s 内并发触发 20 次同一 workflow，每 job sleep 30s

预期结果:
  - 20 次触发全部进入终态
  - running 峰值≤5
  - 总耗时≤15min

验证点:
  - [正向] completed=20
  - [负向] running 峰值不应>5
  - [负向] 不应出现运行静默消失

清理:      无需特殊清理
