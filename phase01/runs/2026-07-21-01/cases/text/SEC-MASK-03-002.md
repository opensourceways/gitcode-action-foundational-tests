用例 ID:   SEC-MASK-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-006
母意图:    —
标题:      Secret 经过 base64 编码后 echo 到日志仍应被脱敏

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 值通过 base64 编码后 echo 到日志
  2. 将 base64 解码后的值再次 echo
  3. 通过 API 拉取 job 日志搜索原始 secret 明文

预期结果:
  - 日志中不出现未经遮蔽的 secret 原始值
  - base64 编码和解码后的输出中，原始值不应以明文出现

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 原始明文值，命中数 = 0
  - [负向] base64 编码后的值若直接 echo，不应泄露 secret 原始值

清理:      none
