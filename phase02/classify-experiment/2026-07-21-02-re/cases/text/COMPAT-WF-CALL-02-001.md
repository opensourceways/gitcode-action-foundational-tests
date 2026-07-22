用例 ID:   COMPAT-WF-CALL-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-061
母意图:    —
标题:      workflow_call 复用差异——嵌套层数、secrets 传递、inputs 类型与 GitHub 对齐

前置条件:
  - 存在可复用的 callee workflow

操作步骤:
  1. 定义 workflow_call 的 callee workflow
  2. 在 caller workflow 中调用并传递 secrets 与 inputs
  3. 观察运行结果

预期结果:
  - workflow_call 应正确传递 inputs 与 secrets
  - 嵌套层数应受文档限制

验证点:
  - [正向] inputs 与 secrets 正确传递到 callee
  - [负向] 超过 2 层嵌套应被拒绝

清理:      重置 fixture 仓库
