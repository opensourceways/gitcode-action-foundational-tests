用例 ID:   REL-FAULT-01-032
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-032
母意图:    —
标题:      故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

前置条件:
  - 具备故障注入能力
  - fixture 仓库可接受破坏性测试

操作步骤:
  1. 触发含 upload-artifact step 的 workflow，在 upload 期间注入网络分区 30 秒

预期结果:
  - upload-artifact step 状态=failure
  - 日志含 network/connection/timeout 或中文等价词
  - 不应无限挂起超过 120 秒

验证点:
  - [正向] upload-artifact step 状态=failure
  - [正向] 日志含网络错误
  - [负向] 不应无限挂起超过 120 秒

清理:      重置 fixture 仓库
