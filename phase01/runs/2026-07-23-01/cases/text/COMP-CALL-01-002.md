用例 ID:   COMP-CALL-01-002
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-006
母意图:    —
标题:      3 层 workflow_call 嵌套应被拒绝

前置条件:
  - 存在 3 层嵌套的可重用 workflow 结构

操作步骤:
  1. 触发顶层主 workflow
  2. 观察第 3 层嵌套调用是否被拒绝

预期结果:
  - 平台在第 3 层调用时报错或阻止执行

验证点:
  - [负向] 运行不应成功完成
  - [非功能] 报错信息应清晰说明最多 2 层限制

清理:      none
