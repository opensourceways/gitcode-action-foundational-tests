用例 ID:   SEC-PRTGT-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-002
母意图:    —
标题:      pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 在 base 分支 workflow 中使用 pull_request_target 触发
  2. 显式 checkout fork PR 的 head sha 并执行脚本
  3. 观察 secrets 是否可被该脚本访问

预期结果:
  - 系统应阻止或限制在 pull_request_target 中直接执行未经审核的 fork PR 代码
  - secrets 不应被不可信代码直接读取

验证点:
  - [负向] 运行日志中不应出现 DEPLOY_TOKEN 明文
  - [正向] 若存在审批机制，未审批状态下 job 应处于挂起或拒绝态

清理:      重置 fixture 仓库
