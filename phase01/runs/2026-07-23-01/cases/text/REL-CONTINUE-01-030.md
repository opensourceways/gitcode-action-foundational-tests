用例 ID:   REL-CONTINUE-01-030
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-030
母意图:    —
标题:      continue-on-error=true——job 失败后 workflow 不应终止

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发含 continue-on-error=true 的失败 job 和下游 job 的 workflow

预期结果:
  - job_a 状态=failure 但 workflow 不终止
  - job_b 正常执行并 success

验证点:
  - [正向] job_a 状态=failure
  - [正向] job_b 状态=success
  - [负向] workflow 不应因 job_a 失败而整体 failure

清理:      无需特殊清理
