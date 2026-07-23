用例 ID:   SEC-MASK-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
母意图:    —
标题:      Secret 日志脱敏不可通过 base64 编码绕过

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，在 job 中对 secret 做 base64 编码后再输出到日志
  2. 触发 workflow 并查看运行日志

预期结果:
  - base64 编码后的 secret 值不应以明文形式出现在日志中
  - 系统应能识别编码后的 secret 并执行脱敏

验证点:
  - [负向] 日志中绝不应出现 base64 编码后的 DEPLOY_TOKEN
  - [非功能] 脱敏机制应覆盖常见编码变换

清理:      重置 fixture 仓库
