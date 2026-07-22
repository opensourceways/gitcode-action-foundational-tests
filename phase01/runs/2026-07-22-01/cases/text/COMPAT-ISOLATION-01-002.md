用例 ID:   COMPAT-ISOLATION-01-002
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-028
母意图:    COMPAT-ISOLATION-01-001
标题:      Runner 复用时的隔离策略与 GitHub ephemeral 语义对齐

前置条件:
  - 仓库已启用 Actions
  - 使用平台托管 Runner

操作步骤:
  1. 触发 workflow，检查以 Runner 标识命名的标记文件是否存在
  2. 若存在，说明同一 Runner 被复用且未清理环境
  3. 对比 GitHub Actions 行为：GitHub 托管 runner 为 ephemeral，每次全新环境

预期结果:
  - GitCode 官方托管 Runner 应表现为环境隔离，不应出现复用标记
  - 若出现复用，应记录为与 GitHub 的兼容性差异

验证点:
  - [正向] 日志显示 FRESH_RUNNER_OR_FIRST_USE
  - [负向] 日志不含 SAME_RUNNER_REUSED

清理:      fixture
