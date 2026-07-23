用例 ID:   COMPAT-PATHS-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-019
标题:      paths 过滤器语义差异：300 文件上限

前置条件: 仓库有 push/pull_request 触发 workflow
操作步骤:
  1. paths: ['src/**'] → 验证仅 src/ 变更时触发
  2. paths-ignore: ['docs/**'] → 验证 docs/ 变更不触发
  3. 变更超 300 文件 → 验证前 300 参与匹配
  4. ! 排除语法验证

预期结果: GitCode paths 按 300 文件上限截断；排除语法正确
验证点:
  - [正向] paths 过滤和 paths-ignore 正确
  - [正向] 300 文件上限行为明确
清理:      fixture
