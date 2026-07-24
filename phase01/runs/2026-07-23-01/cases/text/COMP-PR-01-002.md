用例 ID:   COMP-PR-01-002
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-004
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      pull_request_target 可访问 secrets 且 TOKEN 拥有写权限

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 场景下触发 pull_request_target workflow
  2. workflow 中引用 secrets.DEPLOY_TOKEN

预期结果:
  - workflow 能获取 DEPLOY_TOKEN（日志中脱敏显示为 ***）
  - ATOMGIT_TOKEN 拥有写权限

验证点:
  - [正向] pull_request_target 可访问 secrets
  - [正向] 日志中 secret 显示为 ***（脱敏生效）

清理:      重置 fixture 仓库
