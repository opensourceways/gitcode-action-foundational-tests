用例 ID:   COMP-MALWF-01-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P0
溯源意图:  INTENT-COMP-014
母意图:    —
标题:      恶意 PR 修改 workflow 文件后 pull_request_target 的行为

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR

操作步骤:
  1. fork 贡献者在 PR 中修改 workflow 文件，试图添加恶意步骤（如输出 secret）
  2. PR 触发 pull_request_target 事件
  3. 观察执行的 workflow 版本：是 base 分支的版本还是 PR 中修改的版本

预期结果:
  - pull_request_target 必须使用 base 分支的 workflow 版本
  - PR 中修改的 workflow 文件不应在 pull_request_target 下执行
  - base 分支版本中的权限控制仍然生效

验证点:
  - [负向] 不应执行 PR 中修改的恶意 workflow 步骤
  - [正向] 执行的是 base 分支的 workflow 版本

清理:      fixture
