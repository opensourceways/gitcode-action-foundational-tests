用例 ID:   SEC-SLICE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-008
母意图:    —
标题:      secret 分片输出不应绕过日志脱敏

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中通过字符切片/数组索引将 DEPLOY_TOKEN 分片输出
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 系统识别出分片片段属于 secret 并进行脱敏
  - 运行日志中不出现 DEPLOY_TOKEN 的任何分片明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 的任一分片明文
  - [负向] 日志不含 DEPLOY_TOKEN 完整明文
  - [正向] workflow 执行未被阻塞（仅验证脱敏行为）

清理:      重置 fixture 仓库
