用例 ID:   REL-CPU-01-022
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-022
母意图:    —
标题:      Runner CPU 饱和——small runner 运行 4 个 CPU 密集型进程应完成但耗时延长

前置条件:
  - 仓库具备 small runner 使用权限

操作步骤:
  1. 触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，启动 4 个并行 CPU burn 进程，各运行 60 秒

预期结果:
  - job 状态=success
  - 总耗时约为 120±24 秒
  - 不应被强制终止

验证点:
  - [正向] job 状态=success
  - [非功能] 总耗时 120±24 秒
  - [负向] 不应被系统强制终止

清理:      重置 fixture 仓库
