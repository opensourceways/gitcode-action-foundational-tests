用例 ID:   REL-CONCUR-01-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-004
标题:      concurrency max=1 IGNORE 拒绝超限触发

前置条件: workflow concurrency max=1 exceed-action=IGNORE
操作步骤:
  1. 触发 Run1 进入 in_progress
  2. 立即触发 Run2
  3. 验证 Run2 被拒绝（skipped/cancelled），不排队

预期结果: 新 Run 立即可拒绝终态；无 job 被调度
验证点:
  - [正向] 新 Run 状态 skipped/cancelled
  - [负向] 新 Run 不为 queued 或 in_progress
清理:      none
