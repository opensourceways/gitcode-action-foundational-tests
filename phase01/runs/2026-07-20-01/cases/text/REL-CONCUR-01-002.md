用例 ID:   REL-CONCUR-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-002
标题:      concurrency max=2 QUEUE 排队语义正确

前置条件: workflow concurrency max=2 exceed-action=QUEUE
操作步骤:
  1. 连续触发 5 个 workflow_dispatch
  2. 验证任意时刻 in_progress Run 数 <= 2
  3. 验证 5 个 Run 全部到达 completed
  4. 验证 slot 释放后排队 Run 自动开始

预期结果: 排队语义正确；无 Run 丢失或被饿死
验证点:
  - [正向] in_progress <= 2
  - [正向] 5 个全部完成
清理:      none
