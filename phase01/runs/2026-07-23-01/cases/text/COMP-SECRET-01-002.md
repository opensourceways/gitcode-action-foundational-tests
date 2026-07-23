用例 ID:   COMP-SECRET-01-002
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-012
母意图:    —
标题:      secret 原始值不应以明文出现在标准日志中

前置条件:
  - 仓库配置了 secret TEST_SECRET

操作步骤:
  1. 在 workflow 中通过多种方式输出 secret
  2. 查看运行日志

预期结果:
  - 无论通过何种标准方式引用，secret 原始值均不出现在日志

验证点:
  - [负向] 日志中不包含 secret 原始明文

清理:      重置 fixture 仓库
