用例 ID:   SEC-MASK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-006
标题:      Secret 经过 base64 编码后 echo 到日志仍应被脱敏
前置条件:  仓库配置 Secret DEPLOY_TOKEN
操作步骤:
  1. echo DEPLOY_TOKEN 明文 → 验证基础脱敏
  2. echo DEPLOY_TOKEN | base64 → 验证输出不泄露原始值
  3. base64 编码后解码再 echo → 验证仍被遮蔽
预期结果: base64 编码或解码后的 secret 明文在日志中不出现
验证点:
  - [负向] echo base64(secret) 的输出不含 secret 原始值
  - [负向] 解码后 echo 时 secret 明文被遮蔽
清理:      fixture
