用例 ID:   COMPAT-SCHED-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-020
标题:      schedule 定时触发差异：时区、默认分支、最短间隔

前置条件: 仓库有 schedule workflow；已知 S3x24+TC-391 schedule 不工作
操作步骤:
  1. cron 在 UTC 时区 → 验证按时触发
  2. 非默认分支 schedule → 验证不触发
  3. timezone 字段（GitHub 语法）→ 验证明确报错
预期结果: UTC 时区触发；仅默认分支生效；GitHub timezone 字段报错
验证点:
  - [正向] UTC 时区 cron 触发
  - [正向] 非默认分支不触发
  - [负向] timezone 字段报错
清理:      fixture
