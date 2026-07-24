用例 ID:   REL-QUEUE-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-003
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      concurrency QUEUE 策略——超上限运行应排队等待

前置条件:
  - 仓库已配置 concurrency.max=2 exceed-action=QUEUE 的 workflow

操作步骤:
  1. 同时触发 4 次该 workflow

预期结果:
  - 运行 1-2 进入 in_progress
  - 运行 3-4 进入 queued
  - 前 2 个完成后 3-4 自动启动

验证点:
  - [正向] 4 个运行最终全部 completed(success)
  - [负向] 运行 3-4 不应被丢弃

清理:      无需特殊清理
