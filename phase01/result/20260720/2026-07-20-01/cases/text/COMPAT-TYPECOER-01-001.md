用例 ID:   COMPAT-TYPECOER-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-006
标题:      表达式类型强转规则：contains/== 的松散类型比较行为对标

前置条件: 仓库 workflow 使用表达式比较

操作步骤:
  1. 验证 '' == 0 在 GitCode 中的行为（GitHub: true）
  2. 验证 null 表达式的真值性（GitHub: falsy）
  3. 验证数组中 contains 的匹配行为
  4. 对比同一表达式在 GitCode 和 GitHub 的结果

预期结果: 类型强转规则与 GitHub 一致或文档化差异
验证点:
  - [正向] '' == 0 行为明确
  - [正向] null 真值性明确
  - [负向] 不对 GitHub 行为产生静默差异
清理:      fixture
