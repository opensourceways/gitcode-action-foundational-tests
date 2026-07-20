用例 ID:   REL-CONCUR-02-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-004
标题:      concurrency max=1 且 exceed-action=IGNORE 时，并发超限的触发被直接拒绝

前置条件:
  - workflow 配置 concurrency: { enable: true, max: 1, exceed-action: IGNORE }
  - 已有 1 个 in_progress 的 run

操作步骤:
  1. 先触发一次 push 使 Run1 进入 in_progress
  2. 立即再触发一次 push 产生 Run2
  3. 验证 Run2 立即被拒绝（skipped/cancelled），不排队也不执行

预期结果:
  - Run2 不进入 queued 或 in_progress
  - Run2 状态为 skipped 或有明确终态
  - 无 job 被调度

验证点:
  - [正向] Run2 不进入 queued 或 in_progress
  - [正向] Run2 状态为 skipped/cancelled（有明确终态）
  - [负向] Run2 无任何 job 被调度

清理:      fixture
