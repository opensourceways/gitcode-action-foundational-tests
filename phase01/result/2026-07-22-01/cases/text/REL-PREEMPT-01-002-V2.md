用例 ID:   REL-PREEMPT-01-002-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-006
母意图:    REL-PREEMPT-01-001
标题:      preemption events 配置边界值（10 个）应被系统接受并正常工作

前置条件:
  - 仓库已启用 Actions 且具备 runner 资源
  - 当前 preemption events 允许的最大值为 10

操作步骤:
  1. 在仓库中创建 workflow，配置 `preemption-events: 10`
  2. 提交并推送该 workflow 到默认分支
  3. 触发该 workflow 运行

预期结果:
  - 平台接受该 workflow 配置
  - workflow 成功运行完成，且抢占事件被正确处理

验证点:
  - [正向] workflow 运行状态为 success
  - [正向] 运行日志中无配置错误

清理:      重置 fixture 仓库
