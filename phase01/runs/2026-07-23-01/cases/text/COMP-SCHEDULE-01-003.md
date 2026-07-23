用例 ID:   COMP-SCHEDULE-01-003
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-005
母意图:    —
标题:      cron 间隔短于 5 分钟时被拒绝或降级

前置条件:
  - 仓库具备提交 workflow 的权限

操作步骤:
  1. 配置 cron 间隔为 1 分钟
  2. 提交 workflow

预期结果:
  - 平台拒绝该 workflow 或将其降级为最短间隔

验证点:
  - [负向] 不应允许每分钟触发的 schedule
  - [非功能] 错误信息应说明最短间隔限制

清理:      none
