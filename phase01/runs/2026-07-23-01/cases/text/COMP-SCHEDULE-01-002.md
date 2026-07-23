用例 ID:   COMP-SCHEDULE-01-002
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-005
母意图:    —
标题:      非默认分支的 schedule workflow 不应触发

前置条件:
  - workflow 仅存在于非默认分支

操作步骤:
  1. 在非默认分支创建 schedule workflow
  2. 等待到达 cron 设定时间

预期结果:
  - schedule 事件仅在默认分支生效
  - 非默认分支的 schedule workflow 不应触发

验证点:
  - [负向] 运行列表中不存在该 schedule 触发的运行

清理:      none
