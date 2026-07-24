用例 ID:   SEC-SIDE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-032
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    SEC-SIDE-01-001
标题:      Secret 不经 artifact 侧信道绕过脱敏外泄

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，将 secret 写入文件并上传为 artifact
  2. 触发 workflow 并下载 artifact 检查内容

预期结果:
  - Artifact 中不应包含 secret 明文
  - 若 artifact 包含 secret，应被拦截或遮蔽

验证点:
  - [负向] Secret 明文不应以未遮蔽形式出现在上传的 artifact 中
  - [非功能] 覆盖 artifact 侧信道

清理:      重置 fixture 仓库
