用例 ID:   COMP-PRSYNC-01-002
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-004
母意图:    COMP-PRSYNC-01-001
标题:      fork PR force-push 后 pull_request_target 权限保持验证

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR

操作步骤:
  1. fork PR 初次打开时触发 pull_request_target
  2. fork 贡献者执行 force-push 到 PR 分支
  3. 观察 force-push 后触发的 pull_request_target 是否仍保持权限受控

预期结果:
  - force-push 后触发的 pull_request_target 仍不获取 secrets
  - 权限不因 force-push 而意外提升

验证点:
  - [负向] force-push 后不应意外获取 secret 访问权限
  - [正向] 运行日志显示 SECRET_SAFE_AFTER_SYNC

清理:      fixture
