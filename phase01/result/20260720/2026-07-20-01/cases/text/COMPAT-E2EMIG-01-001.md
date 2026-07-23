用例 ID:   COMPAT-E2EMIG-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-027
标题:      端到端迁移摩擦清单

前置条件: 一个标准 GitHub workflow 搬运到 GitCode
操作步骤:
  1. 搬运含 runs-on:ubuntu-latest、github.*、success()、actions/checkout@v4、permissions GitHub 命名的 workflow
  2. 按迁移清单逐项修改：目录名、runs-on、上下文、表达式、action 引用、permissions、types
  3. 验证修改后 workflow 正常触发执行

预期结果: 搬运后报错包含所有差异点；修改后正常执行
验证点:
  - [正向] 未修改时批量暴露所有差异
  - [正向] 逐项修改后正常执行
  - [非功能] 迁移文档覆盖全部改写点
清理:      fixture
