用例 ID:   REL-CHAOS-NET-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-013
标题:      job 执行中网络分区后 step 应超时失败而非永久 hang

前置条件:
  - step 依赖外网（如 curl https://registry.npmjs.org）
  - step 开始后 30s 封禁 runner 外网出站

操作步骤:
  1. step 执行 apt-get update 和 curl 外网 URL
  2. 执行开始 30s 后封禁 runner 外网出站
  3. 观察 step 是否在合理时间内（≤5min）超时失败

预期结果:
  - 依赖网络的 step 在网络不可用后 ≤5min 内超时失败
  - 日志应含可辨识的网络错误（'connection refused' / 'could not resolve host'）
  - step 不应永久 hang 直到 job timeout（360min）

验证点:
  - [正向] step 在 5min 内失败（exit code != 0）
  - [正向] 日志含网络错误信息
  - [负向] step 不 hang 超过 10min

清理:      fixture
