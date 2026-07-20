用例 ID:   REL-CONCUR-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-002
标题:      concurrency max=2, exceed-action=QUEUE 时 5 个同时触发按排队语义执行

前置条件:
  - concurrency max=2, exceed-action=QUEUE
  - 5 个 workflow_dispatch 同时触发

操作步骤:
  1. 验证任意时刻 in_progress <= 2
  2. 5 个 Run 全部到达 completed
  3. 排队按 FIFO 顺序完成

预期结果:
  - max 限制生效
  - 无排队 Run 饿死
  - 全部完成

验证点:
  - [正向] in_progress <= 2 始终成立
  - [正向] 5 个全部成功
  - [负向] 无 Run 丢弃
  - [非功能] slot 释放->调度间隔 < 30s

清理:      fixture
