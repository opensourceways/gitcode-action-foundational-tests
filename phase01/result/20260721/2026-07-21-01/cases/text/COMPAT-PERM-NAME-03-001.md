用例 ID:   COMPAT-PERM-NAME-03-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-080
标题:      permissions 权限域命名差异：GitCode project/pr/issue/note/repository/hook vs GitHub contents/pull-requests/issues/...

前置条件:
  - workflow 中使用 GitHub 风格的 permissions 域命名

操作步骤:
  1. 写 GitHub 风格 permissions: contents: read
  2. 写 GitHub 风格 permissions: pull-requests: write
  3. 写 GitHub 风格 permissions: actions: write
  4. 观察每种写法的解析行为（报错还是静默忽略）

预期结果:
  - GitHub 命名应明确报错（unknown permission scope）
  - 报错应指引用户使用 GitCode 命名（repository/pr/issue 等）
  - 文档应提供 GitHub→GitCode permissions 映射表

验证点:
  - [正向] GitHub 命名 contents: read 应报错
  - [正向] GitCode 命名 repository: read 应生效
  - [正向] 文档提供完整 permissions 域映射表

清理:      fixture
