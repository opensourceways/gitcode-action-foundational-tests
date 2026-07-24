用例 ID:   COMP-CALL-01-001
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-006
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      2 层 workflow_call 嵌套正常执行

前置条件:
  - 存在可重用的子 workflow（1 层）
  - 主 workflow 调用子 workflow（2 层总计）

操作步骤:
  1. 触发主 workflow
  2. 观察嵌套调用是否成功完成

预期结果:
  - 2 层嵌套 workflow_call 成功执行
  - 子 workflow 的输出正确传递回主 workflow

验证点:
  - [正向] 运行状态成功
  - [正向] 子 workflow 的 step 日志可见

清理:      none
