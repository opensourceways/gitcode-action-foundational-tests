用例 ID:   COMPAT-SCHEDULE-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-020
标题:      schedule 定时触发差异：验证时区限制、默认分支限制、最短间隔

前置条件:
  - 配置 schedule cron 的 workflow
  - 已知 S3×24+TC-391：scheduler 完全不可用

操作步骤:
  1. 验证 cron 在 UTC 时区按表达式触发
  2. 验证仅默认分支上的 workflow 文件被 schedule 触发
  3. 测试使用 GitHub timezone 字段（如 "America/New_York"）的行为
  4. 验证最短 cron 间隔为 5 分钟

预期结果:
  - schedule cron 在 UTC 时区触发
  - 仅默认分支生效
  - GitHub timezone 字段应有明确行为

验证点:
  - [正向] cron 在 UTC 时区按时触发
  - [正向] 非默认分支 workflow schedule 不触发
  - [负向] timezone 字段（GitHub 语法）应有明确行为
  - [负向] schedule 应可实际触发（已知 bug TC-391）

清理:      fixture
