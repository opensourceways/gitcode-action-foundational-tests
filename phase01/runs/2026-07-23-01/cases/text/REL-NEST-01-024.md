用例 ID:   REL-NEST-01-024
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-024
母意图:    —
标题:      workflow_call 嵌套越界——3 层嵌套调用应被拒绝

前置条件:
  - fixture 仓库包含 level1/level2/level3.yml

操作步骤:
  1. 触发主 workflow，尝试 A→B→C→D（3 层嵌套）

预期结果:
  - 第 3 层调用失败
  - 运行状态=failure
  - 日志含嵌套层数或 2 层提示

验证点:
  - [正向] 运行状态=failure
  - [正向] 日志明确提示嵌套超限
  - [负向] 不应死循环或挂起

清理:      无需特殊清理
