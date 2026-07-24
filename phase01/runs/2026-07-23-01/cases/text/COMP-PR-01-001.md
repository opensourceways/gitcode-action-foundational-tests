用例 ID:   COMP-PR-01-001
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-004
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      fork PR 触发 pull_request 时不可读取项目 secrets

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 场景下触发 pull_request workflow
  2. workflow 中尝试引用 secrets.DEPLOY_TOKEN

预期结果:
  - workflow 无法获取 DEPLOY_TOKEN 值
  - 运行日志中 DEPLOY_TOKEN 不出现明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] fork PR 的 pull_request workflow 无 secret 访问权限

清理:      重置 fixture 仓库
