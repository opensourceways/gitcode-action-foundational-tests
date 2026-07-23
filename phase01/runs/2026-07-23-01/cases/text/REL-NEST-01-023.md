用例 ID:   REL-NEST-01-023
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-023
母意图:    —
标题:      workflow_call 嵌套边界——2 层嵌套调用应成功执行

前置条件:
  - fixture 仓库包含 level1.yml 和 level2.yml 两个可重用 workflow

操作步骤:
  1. 触发主 workflow，该 workflow 通过 workflow_call 调用 level1，level1 再调用 level2

预期结果:
  - 3 个 workflow 均成功完成
  - 输入参数在每一层正确传递

验证点:
  - [正向] 最外层运行状态=success
  - [正向] 所有子运行均 success

清理:      无需特殊清理
