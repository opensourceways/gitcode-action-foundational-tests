用例 ID:   REL-CONC-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-002
母意图:    —
标题:      concurrency.max=6 配置应被系统拒绝

前置条件:
  - 仓库具备 workflow 创建权限

操作步骤:
  1. 创建 concurrency.max=6 的 workflow 并保存

预期结果:
  - 系统给出明确校验错误
  - 错误信息包含 max 超出范围提示

验证点:
  - [正向] YAML 校验失败或保存被拒
  - [负向] 不应静默截断为 5

清理:      无需特殊清理
