用例 ID:   SEC-ARTF-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    SEC-ARTF-01-001
标题:      跨仓库 artifact 下载返回 403 或 404

前置条件:
  - fork PR 已上传 artifact

操作步骤:
  1. 在主仓 workflow 中尝试下载 fork PR 的 artifact ID
  2. 查看下载结果

预期结果:
  - 下载返回 404 或权限拒绝
  - 不应静默返回空包或成功

验证点:
  - [负向] 跨仓库 artifact 下载绝不应成功
  - [正向] 返回明确的 404 或 403 错误

清理:      重置 fixture 仓库
