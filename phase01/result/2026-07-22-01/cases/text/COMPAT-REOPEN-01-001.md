用例 ID:   COMPAT-REOPEN-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-032
母意图:    —
标题:      fork PR 关闭后重新打开时 pull_request_target 权限保持

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR，曾被关闭

操作步骤:
  1. 关闭 fork PR
  2. 重新打开该 fork PR
  3. 观察重新打开时触发的 pull_request_target 是否仍使用 base 分支 workflow 并保持权限受控

预期结果:
  - 重新打开后触发的 pull_request_target 仍使用 base 分支 workflow 版本
  - secrets 和写权限仍受控，不因重新打开而意外提升

验证点:
  - [负向] 重新打开后不应意外获取 secret 访问权限
  - [正向] 重新打开后仍使用 base 分支 workflow 版本

清理:      fixture
