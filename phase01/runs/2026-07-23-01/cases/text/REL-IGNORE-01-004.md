用例 ID:   REL-IGNORE-01-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-004
母意图:    —
标题:      concurrency IGNORE 策略——超上限运行应直接执行

前置条件:
  - 仓库已配置 concurrency.max=2 exceed-action=IGNORE 的 workflow

操作步骤:
  1. 同时触发 4 次该 workflow

预期结果:
  - 4 个运行全部进入 in_progress
  - 无 queued 状态

验证点:
  - [正向] 4 个运行全部 completed(success)
  - [负向] 不应出现 queued 状态

清理:      无需特殊清理
