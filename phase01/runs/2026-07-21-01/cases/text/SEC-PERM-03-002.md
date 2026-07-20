用例 ID:   SEC-PERM-03-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    —
标题:      未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限

前置条件:
  - 仓库设置中默认权限为 repository:read（已知配置）
  - workflow 中不声明 permissions 字段

操作步骤:
  1. 创建不声明 permissions 的 workflow
  2. 通过 ATOMGIT_TOKEN 尝试 git push（写操作）
  3. 通过 ATOMGIT_TOKEN 尝试 git clone（读操作）
  4. 修改仓库默认权限为 repository:write，重新触发

预期结果:
  - 未声明 permissions 时 token 权限 = 仓库默认值
  - 默认 read 时 push 被拒绝、clone 成功
  - 默认 write 时 push 和 clone 均成功

验证点:
  - [正向] 仓库默认 read 时 git clone 成功
  - [负向] 仓库默认 read 时 git push 被拒绝
  - [正向] 仓库默认 write 时 git push 成功

清理: fixture
