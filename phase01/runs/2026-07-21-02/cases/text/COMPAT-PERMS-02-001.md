用例 ID:   COMPAT-PERMS-02-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-009
标题:      验证 permissions 权限域命名差异 project/pr/repository vs contents/pull-requests 不兼容

前置条件:
  - 使用 GitCode 和 GitHub 两种权限域名

操作步骤:
  1. permissions: {repository: read} → 可 clone 不可 push
  2. permissions: {pr: write} → 可操作 PR
  3. permissions: read-all / write-all / {} 正确执行
  4. permissions: {contents: read}（GitHub 命名）→ 验证报错
  5. permissions: {pull-requests: write} → 验证报错

预期结果:
  - GitCode 域名正确控制权限
  - GitHub 域名应报错（非静默忽略）

验证点:
  - [正向] repository: read 正确限制
  - [正向] pr: write 正确生效
  - [负向] contents: read 应报错
  - [负向] 无静默忽略权限差异

清理:      fixture
