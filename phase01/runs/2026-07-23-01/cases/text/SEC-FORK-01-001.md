用例 ID:   SEC-FORK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      fork PR 触发 pull_request 时不可读取项目 secrets

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个引用 secrets.DEPLOY_TOKEN 的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 系统阻止 fork PR 访问 DEPLOY_TOKEN，引用时返回空值或安全报错
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] fork PR 的 job 中 secrets 引用为空或不可访问

清理:      重置 fixture 仓库
