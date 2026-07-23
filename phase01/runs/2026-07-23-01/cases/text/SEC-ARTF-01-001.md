用例 ID:   SEC-ARTF-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
母意图:    —
标题:      fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行

前置条件:
  - 仓库支持 artifact 上传下载

操作步骤:
  1. 以 fork 贡献者身份提交一个上传 artifact 的 workflow
  2. 在主仓尝试下载该 artifact

预期结果:
  - 主仓不可通过 artifact ID 下载 fork PR 的 artifact
  - 跨仓库 artifact 下载应返回 404 或权限拒绝

验证点:
  - [负向] 主仓 workflow 绝不应能下载到 fork PR 上传的 artifact
  - [非功能] 跨仓库 artifact 下载应返回 404 或权限拒绝，不应静默返回空包

清理:      重置 fixture 仓库
