用例 ID:   SEC-ISOLATE-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-033
母意图:    —
标题:      并发 workflow 下的 token/secret 隔离安全

前置条件:
  - 存在多个并发 workflow job
  - 各 job 使用不同 secret

操作步骤:
  1. 在同一 runner 上并发运行两个 job
  2. job A 尝试读取 job B 的环境变量
  3. 验证跨 job 隔离

预期结果:
  - 同一 runner 上并发 jobs 之间的 token 和 secret 完全隔离
  - job A 不应能从 job B 的工作区读取环境变量

验证点:
  - [负向] 并发 job A 不应能从同 runner 上 job B 的工作区读环境变量
  - [负向] 并发 job 不应能通过 /proc 读取其他 job 的 process args

清理:      full_instance
