用例 ID:   COMP-SCHEDULE-01-001
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-005
母意图:    —
标题:      合法 cron 在默认分支按时触发

前置条件:
  - workflow 位于默认分支
  - cron 表达式合法

操作步骤:
  1. 配置 schedule 触发 workflow
  2. 等待到达 cron 设定时间

预期结果:
  - workflow 在设定时间被触发
  - 运行成功完成

验证点:
  - [正向] 运行记录存在且 event 为 schedule
  - [正向] 触发时间与 cron 预期 UTC 时间一致

清理:      none
