用例 ID:   COMPAT-EXPRCO-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-006
标题:      表达式类型强转规则：验证空字符串/null/NaN 比较行为是否与 GitHub 一致

前置条件:
  - 使用表达式测试各种边界类型转换
  - 对照 GitHub Actions 的 loose equality 行为

操作步骤:
  1. 测试空字符串 vs 数字：`${{ '' == 0 }}` 的值
  2. 测试 null 真值性：`${{ null }}` 的值
  3. 测试数组中 contains 的类型匹配
  4. 测试 NaN 参与比较的结果
  5. 对比 GitHub 文档声明的类型强转规则

预期结果:
  - 空字符串 == 0 行为明确（GitHub: true）
  - null 为 falsy
  - 未声明差异处应与 GitHub 行为一致

验证点:
  - [正向] 空字符串 '' == 0 结果与 GitHub 一致
  - [正向] null 的真值性为 falsy
  - [正向] contains 数组匹配行为一致
  - [负向] 同一表达式不应在 GitCode 和 GitHub 得到不同布尔结果

清理:      fixture
