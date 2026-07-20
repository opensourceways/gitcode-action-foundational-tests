用例 ID:   COMPAT-STRCASE-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-005
标题:      startsWith/endsWith 大小写敏感性：GitCode 区分大小写

前置条件: 仓库 workflow 使用表达式函数

操作步骤:
  1. startsWith('Hello', 'He') → 验证返回 true
  2. startsWith('Hello', 'hello') → 验证返回 false（区分大小写）
  3. endsWith('Hello', 'LO') → 验证返回 false
  4. contains('Hello', 'ELL') → 记录实际行为（文档未声明）
预期结果: startsWith/endsWith 按文档区分大小写；GitHub 不区分（行为不同）
验证点:
  - [正向] 首字母大小写匹配正确返回 true
  - [正向] 不同大小写返回 false（与 GitHub 行为相反）
  - [正向] contains 大小写行为记录
清理:      fixture
