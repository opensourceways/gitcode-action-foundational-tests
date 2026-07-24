用例 ID:   REL-TIMEOUT-01-010
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-010
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发未声明 timeout-minutes 的 workflow，job 执行 sleep 21660

预期结果:
  - job 在 360 分钟时被终止
  - 状态为 failure
  - 日志含超时信息

验证点:
  - [正向] job 状态=failure
  - [负向] 不应无限运行

清理:      无需特殊清理
