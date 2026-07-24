用例 ID:   REL-NEEDS-01-025
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-025
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      needs 失败传播——上游 job 失败时下游 job 应被 skip

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发含 job_a(失败) 和 job_b(needs: job_a) 的 workflow

预期结果:
  - job_a 状态=failure
  - job_b 状态=skipped
  - job_b 不应执行

验证点:
  - [正向] job_a 状态=failure
  - [正向] job_b 状态=skipped
  - [负向] job_b 不应在 job_a 失败后仍执行

清理:      无需特殊清理
