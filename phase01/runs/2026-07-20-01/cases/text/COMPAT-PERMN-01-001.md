用例 ID:   COMPAT-PERMN-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-009
母意图:    —
标题:      permissions 权限域命名差异：GitCode project/pr/repository vs GitHub contents/pull-requests

前置条件:
  - 仓库配置了默认 permissions 设置
  - 准备两组 workflow：一组使用 GitCode 命名（project/pr/issue/note/repository/hook），另一组使用 GitHub 命名（contents/pull-requests/issues/actions/packages）

操作步骤:
  1. 提交 workflow A，使用 `permissions: { repository: read, pr: write }`（GitCode 命名），触发 push 事件
  2. 提交 workflow B，使用 `permissions: { contents: read }`（GitHub 命名），触发 push 事件
  3. 提交 workflow C，使用 `permissions: { pull-requests: write }`（GitHub 命名），触发 push 事件
  4. 在 workflow B/C 的 job 中尝试 clone 代码，观察是否被解析报错或静默忽略

预期结果:
  - workflow A 正常解析并执行，repository:read 允许 clone，pr:write 允许操作 PR
  - workflow B/C 应在 workflow 解析阶段报错，明确指出 `contents`/`pull-requests` 不是 GitCode 识别的权限项
  - 若平台静默忽略 GitHub 命名的权限项，日志中至少应有 warning 级别提示
  - 不应出现：GitHub 命名权限项被静默忽略后，Token 权限与用户预期不一致

验证点:
  - [正向] `permissions: { repository: read }` 正常生效，可 clone
  - [正向] `permissions: { pr: write }` 正常生效，可操作 PR
  - [负向] `permissions: { contents: read }`（GitHub 命名）应报错而非静默忽略
  - [负向] `permissions: { pull-requests: write }`（GitHub 命名）应报错
  - [正向] `permissions: read-all` / `write-all` / `{}` 快捷语法语义正确
  - [负向] 使用 GitHub 权限域名时不应静默忽略导致权限与预期不符

清理:      fixture
