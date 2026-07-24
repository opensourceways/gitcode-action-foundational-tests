用例 ID:   COMPAT-TARGET-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-032
母意图:    —
标题:      pull_request_target 默认 types 与 GitHub 差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，on 为 `pull_request_target`（不声明 types）
  2. 创建 PR
  3. 观察触发行为

预期结果:
  - GitHub 行为：默认 types 为 opened, synchronize, reopened
  - GitCode 行为：默认 types 可能不同
  - 应明确记录差异

验证点:
  - [正向] 默认 types 下 PR open 应触发 workflow
  - [正向] 默认 types 下 PR synchronize 应触发 workflow

清理:      无
