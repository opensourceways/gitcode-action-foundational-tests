用例 ID:   COMP-FILTER-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-002
标题:      验证 trigger 过滤器 branches/paths/tags 的通配、否定与互斥规则
incorporates: TC-558/559 (branches vs branches-ignore 互斥), TC-236 (paths 不触发)

前置条件:
  - 配置多种过滤规则组合

操作步骤:
  1. branches + branches-ignore 同时使用 → 应报错
  2. paths + paths-ignore 同时使用 → 应报错
  3. branches: ['!main'] 仅否定 → 不触发
  4. branches: ['feature/**', '!feature/experimental'] → 仅匹配分支触发
  5. paths: ['src/**'] → 仅 src/ 变更触发
  6. PR 变更 301 个文件时，第 301 个文件不参与匹配

预期结果:
  - 互斥规则被强制执行
  - 仅否定模式不触发
  - 通配符正确递归匹配
  - 300 文件边界行为可预测

验证点:
  - [正向] 互斥使用时报错
  - [正向] 纯否定模式不触发
  - [正向] ** 和 * 通配语义正确
  - [非功能] 超 300 文件时截断行为可预测

清理:      fixture
