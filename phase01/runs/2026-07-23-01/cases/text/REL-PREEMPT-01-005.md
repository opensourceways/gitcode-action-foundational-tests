用例 ID:   REL-PREEMPT-01-005
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-005
母意图:    —
标题:      preemption events 边界值——配置 10 个应正常解析

前置条件:
  - 仓库具备 workflow 创建权限

操作步骤:
  1. 创建 concurrency.preemption.events 含 10 个事件的 workflow 并保存

预期结果:
  - workflow YAML 校验通过
  - 运行正常触发

验证点:
  - [正向] workflow 保存成功并运行 completed(success)

清理:      无需特殊清理
