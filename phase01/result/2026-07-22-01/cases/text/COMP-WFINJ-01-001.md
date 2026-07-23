用例 ID:   COMP-WFINJ-01-001
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-014
母意图:    COMP-MALWF-01-001
标题:      恶意 fork PR 修改 workflow 文件后 pull_request_target 仍使用 base 分支版本

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在来自 fork 的 PR，且该 PR 修改了 .gitcode/workflows 下的文件

操作步骤:
  1. fork 贡献者提交一个修改 workflow 文件的 PR
  2. 触发 pull_request_target 事件
  3. 在 workflow 中验证当前运行的 workflow 版本是否来自 base 分支

预期结果:
  - 即使 PR 修改了 workflow 文件，pull_request_target 仍使用 base 分支版本
  - atomgit.sha 应与 base.sha 一致

验证点:
  - [正向] 日志显示 USES_BASE_BRANCH
  - [负向] 日志不含 USES_HEAD_BRANCH

清理:      fixture
