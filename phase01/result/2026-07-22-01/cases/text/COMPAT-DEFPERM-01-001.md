用例 ID:   COMPAT-DEFPERM-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-002
母意图:    —
标题:      未声明 permissions 时跨仓库默认 TOKEN 权限验证

前置条件:
  - 仓库未声明 permissions 字段
  - 存在另一个测试目标仓库

操作步骤:
  1. 在当前仓库创建 workflow，未声明 permissions，尝试通过 API 访问另一个仓库的资源
  2. 触发 workflow 并观察访问结果
  3. 对比 GitHub 行为：GitHub 默认 TOKEN 仅对当前仓库有写权限，跨仓库为只读或无权限

预期结果:
  - 未声明 permissions 时，ATOMGIT_TOKEN 对当前仓库的权限应受控
  - 跨仓库访问应被拒绝或仅允许只读操作
  - 默认权限不应过于宽松

验证点:
  - [负向] 跨仓库写操作应被拒绝
  - [正向] 当前仓库只读操作应成功

清理:      fixture
