用例 ID:   SEC-FORK-02-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-029
标题:      fork PR workflow 不应能修改目标仓库的 workflow 文件

前置条件:
  - 仓库配置了默认 permissions
  - 存在来自外部 fork 的 PR

操作步骤:
  1. fork PR workflow 中尝试 git push 修改 .gitcode/workflows/*.yml
  2. fork PR workflow 中尝试通过 API 修改/上传 workflow 文件
  3. 通过正常 PR diff 提交 workflow 文件修改（作为对照）

预期结果:
  - fork PR 的 workflow run 不能直接修改目标仓库 workflow 定义
  - git push 返回 Permission denied
  - API 调用返回 403
  - 正常 PR diff 应可提交 workflow 文件修改（代码审查流程）

验证点:
  - [负向] git push 修改 workflow 文件被拒绝
  - [负向] API 修改 workflow 文件返回 403
  - [正向] PR diff 方式可正常提交 workflow 文件变更

清理:      fixture
