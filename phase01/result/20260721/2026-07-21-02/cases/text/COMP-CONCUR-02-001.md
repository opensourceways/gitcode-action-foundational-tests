用例 ID:   COMP-CONCUR-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-005
标题:      验证并发控制 concurrency max / exceed-action / preemption

前置条件:
  - 配置 concurrency max=2, exceed-action=QUEUE

操作步骤:
  1. 5 个同时 workflow_dispatch 触发
  2. 验证最多 2 个 in_progress，其余排队
  3. max=1 + IGNORE → 新触发被忽略
  4. preemption.enable: true → 新 push 抢占旧 run
  5. job 级 concurrency 覆盖 workflow 级

预期结果:
  - max 限制生效
  - QUEUE 按 FIFO 排队
  - IGNORE 不创建新运行
  - preemption 正确抢占

验证点:
  - [正向] in_progress <= max 值
  - [正向] 排队 runs 最终全部完成
  - [正向] IGNORE 下新触发被拒绝
  - [正向] 抢占后旧 run 被 cancelled

清理:      fixture
