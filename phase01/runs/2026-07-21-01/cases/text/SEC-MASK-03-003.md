用例 ID:   SEC-MASK-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-007
母意图:    —
标题:      Secret 通过子字符串拼接后 echo 到日志应仍被脱敏

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中将 secret 拆分为两半
  2. 通过 shell 拼接两个半段后 echo 到日志
  3. 逐字符循环拼接 secret 后 echo 到日志
  4. 通过 API 拉取 job 日志搜索原始 secret 完整值

预期结果:
  - 拼接后的完整 secret 值不应以明文出现在日志中
  - 逐字符拼接的完整值同样应被遮蔽

验证点:
  - [负向] 日志全文搜索 TEST_SECRET 完整明文值，命中数 = 0
  - [负向] 两半拼接和逐字符拼接 echo 的输出中不出现完整 secret 值

清理:      none
