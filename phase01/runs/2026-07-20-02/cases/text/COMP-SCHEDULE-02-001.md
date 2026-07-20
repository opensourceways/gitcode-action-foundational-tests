用例 ID:   COMP-SCHEDULE-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-021
标题:      验证 schedule 定时触发最短间隔（5 分钟）与 UTC 时区
incorporates: TC-391 (schedule 不工作)

前置条件:
  - 配置不同 cron 表达式的工作流

操作步骤:
  1. cron */5 * * * * → 每 5 分钟触发
  2. cron */2 * * * * → 被拒绝或按 5 分钟执行
  3. 非默认分支的 schedule → 不触发
  4. 验证 UTC 时区

预期结果:
  - 合法 cron 在默认分支上按 UTC 触发
  - 非默认分支不触发
  - 最小间隔 >= 5 分钟
  - schedule 应实际产生运行（TC-391 问题修复确认）

验证点:
  - [正向] 合法 cron 在默认分支触发
  - [正向] 非默认分支不触发
  - [非功能] 调度延迟在可接受范围
  - [负向] schedule 应实际可工作

清理:      fixture
