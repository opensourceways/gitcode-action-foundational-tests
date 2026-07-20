用例 ID:   SEC-PERMS-02-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
标题:      未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限

前置条件:
  - 仓库默认权限设为 repository:read
  - 另一个仓库默认权限设为 repository:write

操作步骤:
  1. 两个仓库的 workflow 均未声明 permissions
  2. 分别尝试 git push

预期结果:
  - 默认 read 仓库的 push 被拒绝
  - 默认 write 仓库的 push 成功
  - 权限行为与仓库默认设置一致

验证点:
  - [正向] repository:read 默认的仓库 push 被拒
  - [正向] repository:write 默认的仓库 push 成功
  - [负向] 权限不被意外放大或缩小

清理:      fixture
