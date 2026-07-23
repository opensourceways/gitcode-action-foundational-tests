用例 ID:   COMP-TIMEOUT-01-001
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-008
母意图:    —
标题:      未声明 timeout-minutes 的 job 在 360 分钟内正常完成

前置条件:
  - workflow 未声明 timeout-minutes

操作步骤:
  1. 触发 workflow
  2. 观察运行是否成功

预期结果:
  - job 在默认 360 分钟超时范围内成功完成

验证点:
  - [正向] 运行状态为 success
  - [非功能] 运行耗时远小于 360 分钟

清理:      none
