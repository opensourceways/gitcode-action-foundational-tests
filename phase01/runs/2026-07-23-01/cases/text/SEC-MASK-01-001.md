用例 ID:   SEC-MASK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    —
标题:      Secret 值在运行日志中必须被自动脱敏为 ***

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，在 run 步骤中直接 echo secrets.DEPLOY_TOKEN
  2. 触发 workflow 并查看运行日志

预期结果:
  - 日志中 DEPLOY_TOKEN 的原值被替换为 ***
  - 日志全文搜索 DEPLOY_TOKEN 原值命中数为 0

验证点:
  - [负向] 日志中绝不应出现 DEPLOY_TOKEN 原值
  - [正向] 脱敏标记 *** 出现在对应位置

清理:      重置 fixture 仓库
