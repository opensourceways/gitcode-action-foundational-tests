用例 ID:   REL-MATRIX-01-026
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-026
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      matrix fail-fast=true——任意 job 实例失败应立即取消其余实例

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发含 3x3 matrix 且 fail-fast=true 的 workflow，其中 1 个实例故意失败

预期结果:
  - 失败 job 状态=failure
  - 其余未完成 jobs 状态=cancelled
  - 总执行时长显著短于全部跑完

验证点:
  - [正向] 失败 job 状态=failure
  - [正向] 其余未完成 jobs 状态=cancelled
  - [负向] 不应继续执行已失败的 matrix 其余实例

清理:      无需特殊清理
