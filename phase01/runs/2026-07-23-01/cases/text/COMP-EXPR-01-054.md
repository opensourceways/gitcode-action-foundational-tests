用例 ID:   COMP-EXPR-01-054
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-180~182
母意图:    —
标题:      字符串函数 contains startsWith endsWith 边界行为

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 step 的 if 条件或 env 中使用 contains / startsWith / endsWith 函数
  2. 覆盖空串、不匹配、边界匹配等场景

预期结果:
  - contains 子串匹配正确，startsWith 前缀匹配正确，endsWith 后缀匹配正确，区分大小写

验证点:
  - [正向] contains 匹配子串返回真
  - [正向] startsWith 匹配前缀返回真
  - [正向] endsWith 匹配后缀返回真
  - [负向] 大小写不匹配返回假

清理:      重置 fixture 仓库
