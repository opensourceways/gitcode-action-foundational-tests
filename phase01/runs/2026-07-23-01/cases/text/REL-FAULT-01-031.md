用例 ID:   REL-FAULT-01-031
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-031
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

前置条件:
  - 具备故障注入能力
  - fixture 仓库可接受破坏性测试

操作步骤:
  1. 触发 workflow，在 job 执行到第 3 个 step 时对 runner 进程注入 SIGKILL

预期结果:
  - job 状态=failure
  - step 1-2 的日志完整可查看
  - step 3 日志不完整或标记为中断

验证点:
  - [正向] job 状态=failure
  - [正向] step 1-2 日志完整
  - [负向] 不应状态=in_progress 挂起超过 5 分钟

清理:      重置 fixture 仓库
