用例 ID:   USE-PR-CHECKS-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-024
母意图:    —
标题:      PR 场景状态回写（Checks/commit status）到 PR 页的可见性与可理解性

前置条件:
  - 存在打开的 PR
  - workflow 配置了 pull_request 触发

操作步骤:
  1. 在 PR 上触发 workflow
  2. 观察 PR 页面是否显示 Checks 或 commit status
  3. 检查状态信息的可理解性

预期结果:
  - PR 页面应显示 workflow 的运行状态
  - 状态信息应包含 workflow 名称与结果

验证点:
  - [正向] PR 页面出现 Checks 或状态标签
  - [nonfunctional] 状态文本可理解

清理:      重置 fixture 仓库
