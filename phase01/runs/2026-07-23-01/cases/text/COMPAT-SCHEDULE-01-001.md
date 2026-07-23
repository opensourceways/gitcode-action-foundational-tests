用例 ID:   COMPAT-SCHEDULE-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-013
母意图:    —
标题:      schedule cron 按 UTC 时间触发

前置条件:
  - 仓库已启用 Actions
  - 默认分支存在

操作步骤:
  1. 在 workflow 中定义 on: schedule 并配置 cron 表达式
  2. 提交并推送该 workflow
  3. 等待或模拟 schedule 触发时刻

预期结果:
  - workflow 应按 UTC 时间触发
  - 若平台支持 timezone 字段，应文档说明；若不支持，cron 应严格按 UTC 解释

验证点:
  - [正向] schedule 事件能正常触发 workflow
  - [非功能] 触发时间应与 UTC 解释一致

清理:      none
