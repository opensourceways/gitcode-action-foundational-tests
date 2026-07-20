用例 ID:   REL-CONCURJ-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-021
标题:      跨 workflow concurrency 不产生死锁

前置条件: 两个不同 workflow 各设 concurrency max=1，各触发 2 次
操作步骤: 同时触发 → 验证无死锁 → 5 分钟内全部到达终态
预期结果: 同 workflow 内同一 job 不出现两个同时 in_progress；无死锁
验证点: [正向] 无死锁；[正向] 全部到达终态
清理: none
