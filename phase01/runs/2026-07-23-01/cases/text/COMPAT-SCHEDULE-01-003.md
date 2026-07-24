用例 ID:   COMPAT-SCHEDULE-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-013
母意图:    —
标题:      schedule 在非默认分支不触发与 GitHub 差异

前置条件:
  - 仓库已启用 Actions
  - 存在非默认分支（如 develop）

操作步骤:
  1. 在 develop 分支创建 schedule workflow
  2. 等待 cron 触发时间

预期结果:
  - GitHub 行为：schedule 仅在默认分支触发
  - GitCode 行为：应同样仅在默认分支触发，若在其他分支触发则差异应被记录

验证点:
  - [负向] develop 分支的 schedule workflow 不应触发
  - [正向] 默认分支的 schedule workflow 正常触发

清理:      无
