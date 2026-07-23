用例 ID:   REL-FAULT-01-033
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-033
母意图:    —
标题:      故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

前置条件:
  - 具备故障注入能力
  - fixture 仓库可接受破坏性测试

操作步骤:
  1. 在 small runner 上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact

预期结果:
  - 写入失败，日志含 No space left on device 或平台等价错误
  - job 状态=failure

验证点:
  - [正向] job 状态=failure
  - [正向] 日志含磁盘满错误

清理:      重置 fixture 仓库
