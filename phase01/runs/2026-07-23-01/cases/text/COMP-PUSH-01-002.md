用例 ID:   COMP-PUSH-01-002
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-003
母意图:    —
标题:      不匹配 branches 的 push 不触发 workflow

前置条件:
  - workflow 配置 branches: [main]

操作步骤:
  1. 向 develop 分支推送代码
  2. 观察 workflow 是否触发

预期结果:
  - push 到 develop 分支不触发 workflow

验证点:
  - [负向] 运行列表中不存在该 push 触发的运行

清理:      none
