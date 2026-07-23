用例 ID:   REL-FAULT-01-034
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-034
母意图:    —
标题:      故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss

前置条件:
  - 具备故障注入能力

操作步骤:
  1. 触发含 cache restore step 的 workflow，在 restore 期间注入 cache 服务 503

预期结果:
  - cache step 状态=success(miss) 或 failure 但不阻断 job
  - 后续 step 正常执行
  - job 不应因 cache 不可用而整体 failure

验证点:
  - [正向] cache step 标记为 miss 或跳过
  - [正向] 后续 step 正常执行
  - [负向] job 不应因 cache 服务不可用而整体 failure

清理:      无需特殊清理
