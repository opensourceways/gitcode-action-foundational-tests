用例 ID:   COMPAT-PR-01-006
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-003
母意图:    —
标题:      PR 目标分支过滤行为差异

前置条件:
  - 仓库已启用 Actions
  - 存在至少一个已配置的 workflow，on 包含 pull_request.branches
  - 测试者持有 maintainer 权限

操作步骤:
  1. 配置 workflow 触发器为 `pull_request.branches: [main]`
  2. 创建一个目标分支为 main 的 PR
  3. 再创建一个目标分支为 develop 的 PR
  4. 观察两者是否触发 workflow

预期结果:
  - GitHub 行为：目标分支匹配时触发，不匹配时不触发
  - GitCode 实际：过滤行为由平台决定是否触发（当前难真测）
  - 应明确记录差异

验证点:
  - [正向] 目标分支为 main 的 PR 应触发 workflow
  - [负向] 目标分支为 develop 的 PR 不应触发 workflow

清理:      无
