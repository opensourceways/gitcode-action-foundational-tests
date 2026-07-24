用例 ID:   SEC-SIDE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-032
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      Secret 不经 output 侧信道绕过脱敏外泄

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，将 secret 写入 ATOMGIT_OUTPUT
  2. 触发 workflow 并检查 output 内容

预期结果:
  - Secret 明文不应以未遮蔽形式出现在 job output 中
  - output 中 secret 值应为 *** 或被拦截

验证点:
  - [负向] Secret 明文不应以未遮蔽形式出现在 job output 中
  - [非功能] 覆盖 output 侧信道

清理:      重置 fixture 仓库
