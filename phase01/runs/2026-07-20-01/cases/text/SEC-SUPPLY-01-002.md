用例 ID:   SEC-SUPPLY-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-029
母意图:    —
标题:      fork PR 的 workflow 不应能修改目标仓库的 workflow 文件

前置条件:
  - 目标仓库 main 分支存在 `.gitcode/workflows/` 目录及其中的 workflow 文件
  - 存在一个来自 fork 的 PR
  - fork PR 的 workflow 在 pull_request 事件下运行（ATOMGIT_TOKEN 仅 read）

操作步骤:
  1. 从 fork 提交 PR，其 workflow job 尝试通过 git push 修改 `.gitcode/workflows/ci.yml`
  2. 尝试通过 API（使用 ATOMGIT_TOKEN）修改或上传 workflow 文件
  3. 尝试通过 API 创建新 workflow 文件到 `.gitcode/workflows/` 目录
  4. 尝试通过 API 修改现有 workflow 文件内容

预期结果:
  - fork PR 触发的 workflow 执行 git push 修改 workflow 文件时应被拒绝
  - fork PR 触发的 workflow 通过 API 修改 workflow 文件时应返回 403
  - fork PR 触发的 workflow 通过 API 创建新 workflow 文件时应返回 403
  - 目标仓库的 `.gitcode/workflows/` 目录内容不被 fork PR 的 run 修改

验证点:
  - [负向] fork PR workflow 中的 git push（修改 workflow YAML）应被拒绝
  - [负向] fork PR workflow 通过 API 修改/上传 workflow 文件应返回 403
  - [负向] fork PR workflow 通过 API 创建新 workflow 文件应返回 403
  - [正向] fork PR 通过正常的 PR diff 修改 workflow 文件（代码审查流程）应正常工作

清理:      fixture
