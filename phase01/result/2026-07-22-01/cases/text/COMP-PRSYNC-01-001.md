用例 ID:   COMP-PRSYNC-01-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P0
溯源意图:  INTENT-COMP-004
母意图:    —
标题:      PR 同步更新时 pull_request_target 权限保持验证

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR

操作步骤:
  1. fork PR 初次打开时触发 pull_request_target，记录权限状态
  2. fork 贡献者推送新 commit 到 PR 分支（同步更新）
  3. 观察同步更新后的 pull_request_target 触发是否仍使用 base 分支 workflow 并保持权限受控

预期结果:
  - 同步更新后触发的 pull_request_target 仍使用 base 分支 workflow 版本
  - secrets 和写权限仍受控，不因同步更新而意外提升

验证点:
  - [负向] 同步更新后不应意外获取 secret 访问权限
  - [正向] 同步更新后仍使用 base 分支 workflow 版本

清理:      fixture
