用例 ID:   COMPAT-WF-NEST-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-021
标题:      workflow_call 嵌套深度限制：验证最多 2 层嵌套，超过应报错

前置条件:
  - 3 个 workflow 文件: A (caller) → B (callee) → C (nested callee)
  - 对比 GitHub 无此硬限制

操作步骤:
  1. 验证 A → B → C（2 层嵌套）正常执行
  2. 验证 A → B → C → D（3 层嵌套）应报错
  3. 验证 A → B 且 B → A（循环调用）应被检测并报错

预期结果:
  - 第 1-2 层 workflow_call 正常执行
  - 第 3 层应报错（非静默忽略）
  - 循环调用被检测并阻止

验证点:
  - [正向] 2 层嵌套正常执行
  - [负向] 3 层嵌套明确报错
  - [负向] 循环调用（A→B→A）应被检测并报错

清理:      fixture
