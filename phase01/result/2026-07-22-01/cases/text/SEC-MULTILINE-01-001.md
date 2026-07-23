用例 ID:   SEC-MULTILINE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-007
母意图:    —
标题:      多行 secret 值输出不应绕过日志脱敏

前置条件:
  - 仓库配置了多行 secret MULTILINE_SECRET（值内含换行符）
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中将 MULTILINE_SECRET 按行输出
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 系统对多行 secret 的每一行均进行脱敏
  - 运行日志中不出现 MULTILINE_SECRET 的任一行明文

验证点:
  - [负向] 日志不含 MULTILINE_SECRET 的任一行明文
  - [负向] 日志不含 MULTILINE_SECRET 完整值
  - [正向] workflow 执行未被阻塞（仅验证脱敏行为）

清理:      重置 fixture 仓库
