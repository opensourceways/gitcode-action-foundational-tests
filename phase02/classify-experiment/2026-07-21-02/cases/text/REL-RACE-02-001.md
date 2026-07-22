用例 ID:   REL-RACE-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-021
标题:      job 级 concurrency 跨 workflow 排程无死锁

前置条件:
  - 2 个不同 workflow，每个有 1 个 job 设 concurrency max=1
  - 每个 workflow 各触发 2 次（共 4 个 Run）

操作步骤:
  1. 同时触发两个不同 workflow 各自 2 次
  2. 观察是否存在跨 workflow 锁争用导致的死锁
  3. 验证 5 分钟内所有 valid job 到达终态或 queued

预期结果:
  - 同 workflow 内同一 job 不会两个实例同时 in_progress
  - 所有 job 在 5 分钟内到达终态
  - 无死锁

验证点:
  - [正向] 同 workflow 内 job 无并发执行
  - [正向] 所有 job 终态或 queued
  - [负向] 无 job 永久 stuck

清理:      fixture
