用例 ID:   COMP-PERM-MIN-03-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-029
标题:      permissions: {} 最小权限语义：验证 ATOMGIT_TOKEN 仅可读仓库

前置条件:
  - workflow 设置 permissions: {}（空对象）

操作步骤:
  1. 配置 permissions: {}
  2. 验证 ATOMGIT_TOKEN 是否可读仓库代码
  3. 尝试用 ATOMGIT_TOKEN 写 PR、写 Issue、读 hook
  4. 所有写操作应被拒绝

预期结果:
  - 文档声称 permissions: {} 仅 repository:read
  - ATOMGIT_TOKEN 可读仓库但不可写 PR/Issue/hook
  - 所有写操作应返回 403/401

验证点:
  - [正向] repository:read 操作成功
  - [负向] PR/Issue/hook 写操作被拒绝

清理:      fixture
