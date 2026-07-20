用例 ID:   COMPAT-EXPRCS-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-005
标题:      验证 startsWith/endsWith 大小写敏感性与 GitHub 相反

前置条件:
  - 使用 startsWith/endsWith/contains 函数

操作步骤:
  1. startsWith('Hello', 'He') → true（首字母匹配）
  2. startsWith('Hello', 'hello') → false（与 GitHub true 相反）
  3. endsWith('Hello', 'LO') → false
  4. contains('Hello', 'ELL') → 确认大小写行为

预期结果:
  - GitCode startsWith/endsWith 区分大小写（与 GitHub 不同）
  - contains 行为文档化

验证点:
  - [正向] startsWith 首字母大写匹配
  - [正向] 小写不匹配（与 GitHub 有意不同）
  - [正向] contains 行为明确

清理:      fixture
