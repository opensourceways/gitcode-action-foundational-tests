用例 ID:   REL-MEM-01-020
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-020
母意图:    —
标题:      Runner 内存边界——small runner 分配 7.5 GB 应成功

前置条件:
  - 仓库具备 small runner 使用权限

操作步骤:
  1. 触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 分配 7.5 GB 内存

预期结果:
  - job 状态=success
  - 内存占用峰值约 7.5 GB

验证点:
  - [正向] job 状态=success
  - [负向] 不应在 7 GB 时 OOM

清理:      重置 fixture 仓库
