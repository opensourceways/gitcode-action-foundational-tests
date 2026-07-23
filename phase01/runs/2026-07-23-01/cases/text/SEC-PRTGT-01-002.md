用例 ID:   SEC-PRTGT-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    SEC-PRTGT-01-001
标题:      pull_request_target 无审批不执行 fork PR 代码

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 在 base 分支 workflow 中使用 pull_request_target 触发
  2. 显式 checkout fork PR 的 head sha
  3. 在无审批状态下触发 workflow

预期结果:
  - 未审批状态下 job 应处于挂起或拒绝态
  - 不应直接执行 fork PR 的代码

验证点:
  - [负向] 绝不应在无审批情况下，让 pull_request_target 的 job 直接执行 fork PR 的构建脚本
  - [正向] 若存在审批机制，未审批状态下 job 应处于挂起或拒绝态

清理:      重置 fixture 仓库
