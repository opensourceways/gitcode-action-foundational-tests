用例 ID:   SEC-MASK-01-006
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-008
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      Secret 日志脱敏不可通过分片输出绕过

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，逐字符或逐小段输出 secret
  2. 触发 workflow 并查看运行日志

预期结果:
  - 即使分片输出，secret 的各片段仍被脱敏
  - 或分片到不可还原长度以下

验证点:
  - [负向] secret 的分片输出绝不应在日志中保留明文
  - [非功能] 脱敏机制应设置最小匹配长度

清理:      重置 fixture 仓库
