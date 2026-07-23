用例 ID:   SEC-CONCAT-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-006
母意图:    —
标题:      secret 通过字符串拼接输出不应绕过日志脱敏

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中将 DEPLOY_TOKEN 与前后缀字符串拼接后输出
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 系统识别出拼接中的 secret 值并进行脱敏
  - 运行日志中不出现 DEPLOY_TOKEN 的明文或拼接后的完整结果

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [负向] 日志不含 secret 拼接后的完整字符串
  - [正向] workflow 执行未被阻塞（仅验证脱敏行为）

清理:      重置 fixture 仓库
