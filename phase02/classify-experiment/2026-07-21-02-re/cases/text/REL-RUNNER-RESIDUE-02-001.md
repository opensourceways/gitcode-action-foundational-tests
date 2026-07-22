用例 ID:   REL-RUNNER-RESIDUE-02-001
维度标签:   [reliability, security]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-033
母意图:    —
标题:      托管 Runner 跨 job 复用的残留污染——去 flaky 隔离验证

前置条件:
  - runner 支持跨 job 复用
  - job-1 在 /tmp 与 workspace 写入状态文件

操作步骤:
  1. job-1 写入特定标记文件与进程环境
  2. job-2 在相同 runner 上启动并检测残留
  3. 重复多次以去 flaky

预期结果:
  - job-2 不应检测到 job-1 的标记文件
  - 环境变量不应跨 job 残留

验证点:
  - [负向] job-2 检测不到 job-1 的标记
  - [正向] 多次运行结果一致

清理:      重置 fixture 仓库
