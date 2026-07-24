用例 ID:   REL-MEM-01-021
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-021
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 内存越界——small runner 分配 9 GB 应被 OOM kill

前置条件:
  - 仓库具备 small runner 使用权限

操作步骤:
  1. 触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 分配 9 GB 内存

预期结果:
  - job 状态=failure
  - 日志含 OOM 或 Killed 信息
  - 不影响同 Runner 其他 job

验证点:
  - [正向] job 状态=failure
  - [正向] 日志含 OOM 或 Killed
  - [负向] 不应导致 Runner 宿主机崩溃

清理:      重置 fixture 仓库
