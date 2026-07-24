用例 ID:   SEC-WCMD-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-028
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，执行 add-mask 命令遮蔽 secret
  2. 触发 workflow 并查看日志中命令的响应

预期结果:
  - workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值
  - 命令执行日志应仅显示命令骨架，不含 payload

验证点:
  - [负向] workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值
  - [非功能] 命令执行日志应仅显示命令本身，不含 secret 原值

清理:      重置 fixture 仓库
