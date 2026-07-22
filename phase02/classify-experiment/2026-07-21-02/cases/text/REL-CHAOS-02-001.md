用例 ID:   REL-CHAOS-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P0
溯源意图:  INTENT-REL-015
标题:      在 job 执行中 kill runner 进程，下游 job 应失败且可重跑恢复

前置条件:
  - jobA → jobB（needs 依赖）
  - jobA 进入 in_progress 后 10s kill runner 进程

操作步骤:
  1. jobA in_progress 后 kill runner agent
  2. 验证调度器心跳超时后 jobA → failure/cancelled
  3. jobB 被 skipped
  4. Re-run failed jobs → 完整成功

预期结果:
  - jobA 在 180s 内到达终态
  - 下游 job skipped
  - 重跑后全部成功

验证点:
  - [正向] jobA 180s 内终态（非 stuck）
  - [正向] 重跑后全部成功
  - [负向] 不 stuck in_progress > 300s

恢复预期:   Re-run failed jobs → 全部 success
清理:      full_instance
