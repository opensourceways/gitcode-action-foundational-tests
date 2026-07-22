用例 ID:   SEC-SECRET-MASK-02-002-V2
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-008
母意图:    INTENT-SEC-006
标题:      多行 Secret 值的逐行脱敏覆盖

前置条件:
  - 仓库配置了 MULTILINE_SECRET（值含换行符）
  - workflow 将多行 secret 输出到日志

操作步骤:
  1. 在 run step 中 echo 多行 secret
  2. 观察每一行的脱敏行为

预期结果:
  - 多行 secret 的每一行都应被脱敏为 ***
  - 换行不应导致脱敏中断

验证点:
  - [负向] 日志不含 MULTILINE_SECRET 的任意一行明文
  - [正向] 日志中出现对应行数的 *** 遮蔽

清理:      重置 fixture 仓库
