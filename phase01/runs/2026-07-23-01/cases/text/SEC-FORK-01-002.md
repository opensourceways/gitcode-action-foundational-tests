用例 ID:   SEC-FORK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    SEC-FORK-01-001
标题:      fork PR 中 secrets 引用返回空值且 job 不崩溃

前置条件:
  - 仓库配置了 secret API_KEY
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个将 secrets.API_KEY 注入环境变量的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - secrets.API_KEY 返回空字符串，环境变量未设置
  - job 正常完成，不因 secret 不可访问而失败

验证点:
  - [负向] 环境变量 API_KEY 为空或未定义
  - [正向] job 状态为成功完成

清理:      重置 fixture 仓库
