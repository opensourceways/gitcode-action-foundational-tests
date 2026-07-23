用例 ID:   COMP-PR-01-003
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-004
母意图:    —
标题:      fork PR 的 pull_request workflow ATOMGIT_TOKEN 仅 read 权限

前置条件:
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 的 pull_request workflow 中尝试使用 ATOMGIT_TOKEN 推送代码或评论 PR

预期结果:
  - 写操作因权限不足而失败
  - ATOMGIT_TOKEN 仅拥有 read 权限

验证点:
  - [负向] 写操作（如推送、评论）应失败
  - [正向] ATOMGIT_TOKEN 权限为 read-only

清理:      重置 fixture 仓库
