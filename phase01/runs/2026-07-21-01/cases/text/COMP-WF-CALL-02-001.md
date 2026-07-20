用例 ID:   COMP-WF-CALL-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-016
标题:      验证可重用工作流 workflow_call 的调用传参与 2 层嵌套限制

前置条件:
  - 配置 A → call B（workflow_call）
  - B 配置 on.workflow_call.inputs 和 outputs

操作步骤:
  1. 调用方 with: 传 inputs → 被调用方 ${{ inputs.key }} 可读
  2. 调用方 secrets: 传 secrets → 被调用方可读
  3. 被调用方 outputs 在调用方 needs 可读
  4. 2 层嵌套（A→B→C）→ 第 3 层拦截

预期结果:
  - inputs 和 secrets 传参正确
  - outputs 回传正确
  - 第 3 层嵌套明确报错

验证点:
  - [正向] inputs/secrets 传参正确到达
  - [正向] outputs 正确回传
  - [负向] 第 3 层 → 明确报错

清理:      fixture
