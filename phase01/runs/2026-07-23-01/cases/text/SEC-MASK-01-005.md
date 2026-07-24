用例 ID:   SEC-MASK-01-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-007
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      Secret 日志脱敏不可通过多行值输出绕过

前置条件:
  - 仓库配置了多行 secret MULTI_LINE_SECRET

操作步骤:
  1. 提交一个 workflow，直接 echo 多行 secret 到日志
  2. 触发 workflow 并查看运行日志

预期结果:
  - 多行 secret 的每一行在日志中均被脱敏
  - 换行符不应成为脱敏边界

验证点:
  - [负向] 多行 secret 的任一行均不应以明文出现在日志中
  - [非功能] 脱敏引擎应支持跨行匹配或整值匹配

清理:      重置 fixture 仓库
