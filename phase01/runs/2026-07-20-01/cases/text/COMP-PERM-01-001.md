用例 ID:   COMP-PERM-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-015
母意图:    —
标题:      验证 permissions 权限模型的 6 个权限域与快捷语法

前置条件:
  - 仓库配置了至少 1 个项目级 Secret（如 DEPLOY_KEY）
  - 仓库设置中默认 permissions 可配置
  - 准备至少 3 个 workflow 文件，分别使用不同的 permissions 声明

操作步骤:
  1. 提交 workflow A，声明 `permissions: {}`（空），在 job 中尝试 `git push` 到目标仓库
  2. 提交 workflow B，声明 `permissions: { repository: read, pr: write }`，在 job 中尝试 clone 代码并创建 PR 评论
  3. 提交 workflow C，声明 `permissions: write-all`，在 job 中尝试读取 Secret 并推送代码

预期结果:
  - workflow A：`permissions: {}` 下 ATOMGIT_TOKEN 仅有 `repository:read` 最小默认权限，git push 被拒绝
  - workflow B：可 clone 代码（repository:read），可创建 PR 评论（pr:write）
  - workflow C：write-all 展开到全部 6 个域均为 write
  - 快捷语法 `read-all` 正确展开到全部域为 read
  - 未声明 permissions 时，Token 权限等于仓库设置中的默认值

验证点:
  - [正向] `permissions: {}` 下 git clone 正常成功
  - [负向] `permissions: {}` 下 git push 被拒绝（403 或 Permission denied）
  - [负向] `permissions: {}` 下通过 API 创建 PR 评论被拒绝
  - [正向] `permissions: { pr: write }` 下通过 API 评论 PR 成功
  - [负向] `permissions: { pr: none }` 下尝试写 PR 被拒绝
  - [正向] `permissions: read-all` / `write-all` 快捷语法正确展开
  - [正向] 未声明 permissions 时 Token 权限与仓库默认设置一致

清理:      fixture
