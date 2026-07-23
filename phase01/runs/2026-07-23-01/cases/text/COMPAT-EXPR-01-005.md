```
用例 ID:   COMPAT-EXPR-01-005
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-006
母意图:    —
标题:      contains 表达式空值与空字符串边界

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个 workflow，在 step 中使用 contains 表达式测试边界情况
  2. 包括 contains('', 'a')、contains('abc', '')、以及包含 null/未定义变量的场景
  3. 手动触发并观察输出结果

预期结果:
  - contains 表达式对空字符串和空值有确定性的返回值
  - 验证边界行为与 GitHub Actions 是否一致

验证点:
  - [正向] 空字符串包含任意非空子串返回 false
  - [正向] 任意字符串包含空子串返回 true（若与 GitHub 行为一致）
  - [负向] 空值场景不应导致表达式解析崩溃

清理:      重置 fixture 仓库
```
