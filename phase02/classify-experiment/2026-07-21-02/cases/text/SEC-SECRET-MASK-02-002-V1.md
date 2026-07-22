用例 ID:   SEC-SECRET-MASK-02-002-V1
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-007
母意图:    INTENT-SEC-006
标题:      Secret 字符串拼接/分片输出时仍应被脱敏

前置条件:
  - 仓库配置了 SPLIT_SECRET
  - workflow 将 secret 拆分为多段输出

操作步骤:
  1. 在 run step 中将 secret 的前半段与后半段分别 echo
  2. 在 run step 中将 secret 与已知字符串拼接后 echo

预期结果:
  - 拼接后的完整 secret 仍应被脱敏
  - 分片输出的 secret 片段也应被脱敏

验证点:
  - [负向] 日志不含 SPLIT_SECRET 明文
  - [负向] 日志不含拼接后的完整 secret

清理:      重置 fixture 仓库
