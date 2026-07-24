用例 ID:   COMPAT-PERM-01-005
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-030
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      permissions 空对象时 ATOMGIT_TOKEN 默认权限范围差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，声明 `permissions: {}`
  2. 在 run 步骤中尝试使用 ATOMGIT_TOKEN 进行读操作和写操作
  3. 触发 workflow

预期结果:
  - GitHub 行为：permissions 为空对象时，GITHUB_TOKEN 仅拥有 metadata read 权限
  - GitCode 行为：应最小化权限，不应默认赋予写权限

验证点:
  - [正向] 读操作成功
  - [负向] 写操作被平台拒绝

清理:      无
