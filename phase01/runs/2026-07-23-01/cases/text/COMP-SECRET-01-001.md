用例 ID:   COMP-SECRET-01-001
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-012
母意图:    —
标题:      echo secret 在日志中被脱敏为 ***

前置条件:
  - 仓库配置了 secret TEST_SECRET

操作步骤:
  1. 在 workflow 中执行 echo ${{ secrets.TEST_SECRET }}
  2. 查看运行日志

预期结果:
  - 日志中 secret 值显示为 ***

验证点:
  - [正向] 日志中包含 *** 而非真实 secret 值

清理:      重置 fixture 仓库
