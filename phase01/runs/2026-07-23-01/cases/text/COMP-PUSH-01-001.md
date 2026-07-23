用例 ID:   COMP-PUSH-01-001
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-003
母意图:    —
标题:      匹配 branches 的 push 正确触发 workflow

前置条件:
  - workflow 配置 branches: [main]

操作步骤:
  1. 向 main 分支推送代码
  2. 观察 workflow 是否触发

预期结果:
  - push 到 main 分支触发 workflow 运行

验证点:
  - [正向] 运行记录存在且 event 为 push
  - [正向] head_branch 为 main

清理:      none
