用例 ID:   SEC-MASK-01-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-007
标题:      Secret 通过子字符串拼接后 echo 到日志应仍被脱敏
前置条件:  仓库配置 Secret DEPLOY_TOKEN
操作步骤:
  1. 将 DEPLOY_TOKEN 拆为两半再拼接 echo
  2. 逐字符拼接 secret 再输出
预期结果: 完整 secret 明文不出现在日志中
验证点:
  - [负向] 拼接 echo 后日志不出现完整 secret 值
  - [负向] 日志全文搜索 secret 明文命中数=0
清理:      fixture
