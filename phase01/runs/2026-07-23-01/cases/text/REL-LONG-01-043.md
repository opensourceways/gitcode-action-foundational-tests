用例 ID:   REL-LONG-01-043
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-043
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发 timeout-minutes=360 的 workflow，job 运行 350 分钟并每 60 秒输出心跳日志

预期结果:
  - job 状态=success
  - 运行期间每 60 秒至少输出 1 行日志
  - 不应在 350 分钟前被误判为死进程

验证点:
  - [正向] job 状态=success
  - [正向] 心跳日志间隔≤60 秒
  - [负向] 不应在 350 分钟前被终止

清理:      无需特殊清理
