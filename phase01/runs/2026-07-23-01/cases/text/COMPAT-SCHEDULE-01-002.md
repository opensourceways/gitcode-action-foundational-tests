用例 ID:   COMPAT-SCHEDULE-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-013
母意图:    COMPAT-SCHEDULE-01-001
标题:      schedule 不支持 timezone 字段差异

前置条件:
  - 仓库已启用 Actions
  - 默认分支存在

操作步骤:
  1. 在 workflow 中定义 on: schedule 并配置 cron 表达式的同时添加 timezone 字段
  2. 提交并推送该 workflow
  3. 观察平台校验行为

预期结果:
  - 平台应对不支持的 timezone 字段给出明确的校验错误或静默忽略
  - 错误信息应提示 timezone 字段不被支持

验证点:
  - [负向] 不应因 timezone 字段导致不可预期的行为
  - [正向] 错误信息应明确指出 timezone 字段不支持或文档说明忽略策略

清理:      fixture
