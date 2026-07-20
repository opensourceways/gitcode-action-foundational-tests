用例 ID:   SEC-RUNNER-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-056
母意图:    —
标题:      Self-hosted runner 在 job 结束后应执行 workspace 清理

前置条件:
  - 存在 self-hosted runner
  - 连续多个 job 在该 runner 上执行

操作步骤:
  1. job A 在 workspace 写入文件
  2. job A 结束后 job B 在同一个 self-hosted runner 上执行
  3. 验证 job B 是否可看到 job A 的残留文件

预期结果:
  - job B 不应能看到 job A 的 workspace 文件
  - 平台应提供 runner cleanup 行为的文档说明

验证点:
  - [负向] job B 不应能看到 job A 的 workspace 文件
  - [正向] 平台文档说明 runner 类型及其清理行为

清理:      full_instance
