用例 ID:   SEC-CONCAT-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-006
母意图:    —
标题:      secret 通过 shell 插值拼接不应绕过日志脱敏

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中通过 shell 变量插值将 DEPLOY_TOKEN 嵌入字符串
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 系统识别出插值后的 secret 值并进行脱敏
  - 运行日志中不出现 DEPLOY_TOKEN 明文及其插值结果

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [负向] 日志不含 secret 插值后的完整字符串
  - [正向] workflow 执行未被阻塞（仅验证脱敏行为）

清理:      重置 fixture 仓库
