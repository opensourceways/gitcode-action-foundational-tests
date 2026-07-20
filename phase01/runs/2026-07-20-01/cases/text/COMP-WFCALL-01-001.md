用例 ID:   COMP-WFCALL-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-016
母意图:    —
标题:      验证可重用工作流 workflow_call 的调用传参与 2 层嵌套限制
前置条件:  仓库存在可重用 workflow 文件
操作步骤:
  1. 调用方通过 with 传 inputs、secrets 传 secrets
  2. 验证被调用方正确接收
  3. 构造 A→B→C 三层嵌套，验证第 3 层被拦截
  4. 被调用方 outputs 在调用方可读
  5. 整合 COMPAT-021 的 2 层 pass / 3 层 reject 验证（含循环调用检测）
预期结果:
  - inputs/secrets 传参正确到达
  - 2 层嵌套正常；第 3 层明确报错
  - outputs 在调用方可读
  - 循环调用（A call B call A）被检测并阻止
验证点:
  - [正向] inputs 传参和 secrets 透传正确
  - [正向] 2 层 OK
  - [负向] 第 3 层明确报错
  - [负向] 循环调用被检测并阻止（COMPAT-021 合并内容）
清理:      fixture
