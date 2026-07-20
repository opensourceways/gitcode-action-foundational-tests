用例 ID:   COMP-SCHEDULE-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-021
标题:      验证 workflow 调度延迟与 schedule 最短间隔约束

前置条件:
  - 仓库配置了 schedule workflow
  - 已知现有用例 S3x24+TC-391 报告 schedule 完全不工作

操作步骤:
  1. 配置 cron */5 * * * *（每 5 分钟合法间隔）
  2. 配置 cron */2 * * * *（每 2 分钟非法间隔）
  3. 在默认分支上等待 schedule 触发
  4. 在非默认分支配置 schedule → 验证不触发
  5. 观察实际触发时间与 cron 表达式的偏差

预期结果:
  - 合法 cron 在默认分支上按 UTC 时区触发
  - 非默认分支的 schedule 不触发
  - cron */2 * * * * 被拒绝或按最小 5 分钟间隔执行
  - 调度延迟在文档声明的"数分钟"范围内
  - 多次触发间隔 >= 5 分钟

验证点:
  - [正向] 合法 cron 在默认分支触发
  - [正向] 非默认分支 schedule 不触发
  - [负向] */2 间隔被拒绝或按 5 分钟最小化
  - [非功能] 调度延迟在合理范围内

清理:      fixture
