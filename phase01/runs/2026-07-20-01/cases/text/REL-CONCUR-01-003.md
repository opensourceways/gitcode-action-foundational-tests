用例 ID:   REL-CONCUR-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-003
标题:      concurrency max=1 CANCEL 抢占取消旧 Run

前置条件: workflow concurrency max=1 exceed-action=CANCEL
操作步骤:
  1. 触发 Run1（含 sleep 180 长步骤）
  2. Run1 执行中触发 Run2
  3. 验证 Run1 被 cancelled，Run2 进入执行

预期结果: 旧 Run 被取消；新 Run 正常执行；无并发冲突
验证点:
  - [正向] 旧 Run 状态 cancelled
  - [正向] 新 Run 正常执行
  - [负向] 新旧 Run 不同时 in_progress
清理:      none
