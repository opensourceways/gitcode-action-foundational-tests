用例 ID:   COMP-CONCUR-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-005
母意图:    —
标题:      验证并发控制: concurrency max / exceed-action / preemption

前置条件:  仓库支持 concurrency 配置

操作步骤:
  1. 配置 max:3 + exceed-action:QUEUE，触发 5 个 workflow_dispatch
  2. 配置 max:1 + exceed-action:IGNORE，触发额外 run
  3. 配置 preemption.enable:true + events:[push]，验证抢占

预期结果:
  - max 限制下同时运行数不超过 max
  - QUEUE 策略下超额排队并按序执行
  - IGNORE 策略下超额触发被忽略
  - preemption 抢占旧 run

验证点:
  - [正向] 并发数不超过 max
  - [正向] QUEUE 策略 FIFO 排队
  - [正向] IGNORE 策略拒绝超额触发
  - [正向] preemption 正确抢占

清理:      fixture
