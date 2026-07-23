```
用例 ID:   COMPAT-EXPR-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-004
母意图:    —
标题:      success() 函数的处理行为差异

前置条件:
  - 仓库已启用 GitCode Action

操作步骤:
  1. 提交一个 workflow，在 step 中尝试使用 success() 函数形式的表达式
  2. 对比平台对 success() 与 bare success 的解析差异
  3. 手动触发并观察运行结果

预期结果:
  - 平台可能对 success() 函数与 bare success 关键字有不同的支持策略
  - 记录并验证实际行为与 GitHub Actions 的兼容性差异

验证点:
  - [正向] 若支持，表达式返回布尔结果
  - [负向] 若不支持，应有表达式解析错误或降级行为

清理:      重置 fixture 仓库
```
