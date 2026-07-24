用例 ID:   REL-FAULT-01-035
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-035
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误

前置条件:
  - 具备故障注入能力

操作步骤:
  1. 触发含 download-artifact step 的 workflow，在 download 期间注入服务 503

预期结果:
  - download-artifact step 状态=failure
  - 日志含 503/service unavailable 或中文等价词
  - job 状态=failure

验证点:
  - [正向] download-artifact step 状态=failure
  - [正向] 日志含服务不可用错误
  - [正向] job 状态=failure

清理:      无需特殊清理
