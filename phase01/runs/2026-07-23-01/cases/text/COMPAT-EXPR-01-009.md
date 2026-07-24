用例 ID:   COMPAT-EXPR-01-009
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-009
参照来源:  inputs/github-reference/reference/workflow-syntax.md; inputs/gitcode-spec/COMPAT-NOTES.md
母意图:    —
标题:      loose equality 跨类型强制求值差异

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中使用 eq 表达式比较不同原始类型的值（如字符串与数字、布尔与字符串）
  2. 提交并触发 workflow
  3. 观察求值结果是否与 GitHub Actions 一致

预期结果:
  - 跨类型比较行为应与 GitHub Actions 的 loose equality 语义一致
  - 若存在差异，应明确记录强制转换规则

验证点:
  - [正向] 表达式求值不报错
  - [非功能] 跨类型比较结果应与 GitHub Actions 行为一致

清理:      fixture
