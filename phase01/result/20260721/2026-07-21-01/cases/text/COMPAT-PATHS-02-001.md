用例 ID:   COMPAT-PATHS-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-019
标题:      验证 paths 过滤器 300 文件上限与 GitHub 3000 阈值差异
incorporates: TC-236 (paths 不触发)

前置条件:
  - 配置 paths 过滤规则，PR 变更超 300 文件

操作步骤:
  1. 变更 <=300 文件时 paths 行为与 GitHub glob 语义一致
  2. 变更 >300 文件时前 300 个参与匹配
  3. ! 排除语法行为正确
  4. 验证 paths 条件满足时确实触发（TC-236 修复确认）

预期结果:
  - 300 文件截断行为与 GitCode 声明一致
  - 排除语法正确
  - paths 应可靠触发

验证点:
  - [正向] <=300 文件 glob 匹配正确
  - [正向] >300 文件截断可预测
  - [负向] 条件满足应触发

清理:      fixture
