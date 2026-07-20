用例 ID:   SEC-FORKPR-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    —
标题:      fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读

前置条件:
  - 主仓库有 pull_request 触发 workflow
  - workflow 声明 permissions: write-all
  - 来自 fork 的 PR

操作步骤:
  1. fork PR 触发 pull_request workflow
  2. 在 workflow 中通过 ATOMGIT_TOKEN 尝试 git push
  3. 在 workflow 中通过 ATOMGIT_TOKEN 尝试 API 创建 PR 评论
  4. 在 workflow 中尝试 git clone

预期结果:
  - fork PR 下 ATOMGIT_TOKEN 仅具 repository:read，无论 permissions 声明
  - git push 被拒绝（403/Permission denied）
  - API 写操作被拒绝
  - git clone 正常

验证点:
  - [正向] git clone 正常完成
  - [负向] git push 应被拒绝
  - [负向] API 创建 PR 评论应返回 403
  - [负向] fork PR 不应能读取项目级 Secret

清理: fixture
