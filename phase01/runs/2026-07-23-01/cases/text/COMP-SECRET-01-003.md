用例 ID:   COMP-SECRET-01-003
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-012
母意图:    —
标题:      base64 编码后的 secret 是否仍被脱敏

前置条件:
  - 仓库配置了 secret TEST_SECRET

操作步骤:
  1. 在 workflow 中对 secret 进行 base64 编码后输出
  2. 查看运行日志

预期结果:
  - 记录实际行为：编码后是否仍被脱敏

验证点:
  - [非功能] 记录 base64 编码输出是否被脱敏

清理:      重置 fixture 仓库
