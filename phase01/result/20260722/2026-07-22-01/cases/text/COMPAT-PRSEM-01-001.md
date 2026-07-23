用例 ID:   COMPAT-PRSEM-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-032
母意图:    COMPAT-REOPEN-01-001
标题:      fork PR 关闭后重新打开时 pull_request_target 语义一致性

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR

操作步骤:
  1. fork PR 初次打开时触发 pull_request_target
  2. 关闭该 PR
  3. 重新打开该 PR，再次触发 pull_request_target
  4. 观察重新打开后的权限和 workflow 来源

预期结果:
  - 重新打开后触发的 pull_request_target 仍不获取 secrets
  - 仍使用 base 分支 workflow 版本
  - 行为与 GitHub pull_request_target 语义一致

验证点:
  - [负向] 重新打开后不应意外获取 secret 访问权限
  - [正向] 日志显示 SECRET_SAFE_ON_REOPEN
  - [正向] 日志显示 BASE_BRANCH_ON_REOPEN

清理:      fixture
