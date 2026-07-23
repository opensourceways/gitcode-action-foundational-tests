用例 ID:   SEC-SUPPLY-03-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-032
母意图:    —
标题:      reusable workflow 调用方传入的 secrets 不应被被调用方泄露到日志

前置条件:
  - 存在 workflow_call 的子 workflow
  - 调用方传入 secrets

操作步骤:
  1. 调用方通过 secrets 将 TEST_SECRET 传给被调用方
  2. 被调用方 echo 该 secret
  3. 通过 API 拉取日志搜索 secret 明文

预期结果:
  - secret 在被调用方日志中同等受脱敏保护
  - 日志搜索 secret 明文命中数 = 0

验证点:
  - [负向] 被调用方 echo 调用方传入的 secret，日志应显示 ***
  - [负向] 被调用方将传入 secret base64 编码后输出不应泄露

清理:      none
