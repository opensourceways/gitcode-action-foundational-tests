用例 ID:   COMPAT-ISOLATION-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-028
母意图:    —
标题:      Runner 环境隔离与复用策略兼容性确认

前置条件:
  - 仓库已启用 Actions
  - 具备官方托管 Runner 与自托管 Runner 两种场景

操作步骤:
  1. 在 workflow 中连续运行两个 job，job A 写入敏感文件到 /tmp 和 workspace
  2. job B 读取 /tmp 和 workspace 验证是否残留
  3. 对比 GitHub Actions 行为：GitHub 托管 runner 是 ephemeral，每次全新环境

预期结果:
  - GitCode 官方托管 Runner 应表现为环境隔离（无残留）
  - 若存在复用，文档应明确说明复用策略及清理保证
  - 验证结果应与 GitHub ephemeral 行为对齐，或有明确差异声明

验证点:
  - [负向] job B 不应读取到 job A 的残留文件
  - [正向] 若发现残留，应记录为兼容性差异并上报

清理:      fixture
