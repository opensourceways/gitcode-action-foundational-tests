用例 ID:   REL-PREEMPT-01-006
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-006
母意图:    —
标题:      preemption events 越界值——配置 11 个应被拒绝

前置条件:
  - 仓库具备 workflow 创建权限

操作步骤:
  1. 创建 concurrency.preemption.events 含 11 个事件的 workflow

预期结果:
  - 系统在解析阶段报错
  - 错误信息包含 events 数量超限提示

验证点:
  - [正向] 明确报错
  - [负向] 不应静默截断

清理:      无需特殊清理
