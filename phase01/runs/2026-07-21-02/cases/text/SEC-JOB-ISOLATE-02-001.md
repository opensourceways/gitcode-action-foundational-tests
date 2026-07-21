用例 ID:   SEC-JOB-ISOLATE-02-001
维度标签:   [security, reliability]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-033
母意图:    —
标题:      同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见）

前置条件:
  - 同一 runner 上并发执行两个 job
  - job-1 创建标记文件并写入进程信息

操作步骤:
  1. job-1 与 job-2 同时运行
  2. job-1 在 /tmp 与 workspace 创建隔离标记
  3. job-2 检查 /tmp 与 workspace 是否存在 job-1 的标记

预期结果:
  - 并发 job 之间不应看到对方的进程、文件或环境变量

验证点:
  - [负向] job-2 检测不到 job-1 的进程
  - [负向] job-2 读取不到 job-1 的文件

清理:      重置 fixture 仓库
