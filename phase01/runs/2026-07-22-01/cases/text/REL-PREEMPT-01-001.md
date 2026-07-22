用例 ID:   REL-PREEMPT-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-006
母意图:    —
标题:      preemption events 配置越界值（11 个）应被系统拒绝

前置条件:
  - 仓库已启用 Actions 且具备 runner 资源
  - 当前 preemption events 允许的最大值为 10

操作步骤:
  1. 在仓库中创建 workflow，配置 `preemption-events: 11`
  2. 提交并推送该 workflow 到默认分支
  3. 尝试触发该 workflow 运行

预期结果:
  - 平台拒绝该 workflow 配置，或运行直接失败并返回配置错误
  - 错误信息中明确指出 preemption events 超出允许范围

验证点:
  - [负向] 不允许成功运行配置 11 个抢占事件的 workflow
  - [正向] 错误信息包含越界提示

清理:      重置 fixture 仓库
