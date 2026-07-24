用例 ID:   COMP-PERMS-01-003
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-013
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      fork PR 的 pull_request 下声明 write 仍仅 read

前置条件:
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 的 pull_request workflow 中声明 repository: write
  2. 尝试使用 ATOMGIT_TOKEN 推送代码

预期结果:
  - 写操作因权限不足失败
  - fork PR 的 TOKEN 权限不受 permissions 声明影响

验证点:
  - [负向] 写操作应失败
  - [正向] 系统应强制 fork PR TOKEN 为 read-only

清理:      重置 fixture 仓库
