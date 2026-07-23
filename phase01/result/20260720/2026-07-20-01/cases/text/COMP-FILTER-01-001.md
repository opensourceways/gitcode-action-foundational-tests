用例 ID:   COMP-FILTER-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-002
母意图:    —
标题:      验证 trigger 过滤器: branches/paths/tags 的通配、否定与互斥规则

前置条件:
  - 仓库多分支结构（main / feature/* / feature/experimental）
  - 准备多个使用不同过滤器配置的 workflow 文件

操作步骤:
  1. 配置 branches 与 branches-ignore 同时使用 → 应报错
  2. 配置 paths 与 paths-ignore 同时使用 → 应报错
  3. 配置 branches: ['!main'] 仅否定模式 → 不应触发
  4. 配置 branches: ['feature/**', '!feature/experimental'] → 仅 feature 分支触发
  5. 配置 paths: ['src/**'] → 仅 src/ 下有变更时触发
  6. PR 变更超过 300 个文件时观察 paths 匹配行为

预期结果:
  - branches/branches-ignore 互斥时报错
  - paths/paths-ignore 互斥时报错
  - 仅否定模式不触发
  - `**` 通配递归匹配多级目录
  - `*` 通配仅匹配单级
  - 超 300 文件变更时第 301+ 文件不参与 paths 匹配

验证点:
  - [正向] 互斥配置时报明确错误
  - [正向] `**` vs `*` 通配语义正确
  - [正向] `!` 排除语法正确
  - [非功能] 超过 300 文件变更时 paths 行为可预测

清理:      fixture
