用例 ID:   REL-STATE-01-058
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-058
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 状态机正确性——空闲/运行/离线转换与时序一致性

前置条件:
  - 仓库具备 runner 状态查询权限

操作步骤:
  1. 对同一 runner 连续执行触发→观察→等待→触发循环 5 轮

预期结果:
  - 状态序列符合 idle→running→idle
  - 转换时延有界

验证点:
  - [正向] 状态序列正确
  - [非功能] idle→running≤30s
  - [非功能] running→idle≤60s

清理:      无需特殊清理
