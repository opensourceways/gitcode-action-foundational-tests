用例 ID:   SEC-ISOLATE-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-047
母意图:    —
标题:      共享文件系统不应跨 job 残留敏感文件

前置条件:
  - 存在多个 push workflow job
  - 各 job 在不同时间执行

操作步骤:
  1. job A 在 /tmp 和 $HOME 写入含敏感内容的文件
  2. job A 结束后，job B 尝试查找这些文件
  3. 验证跨 job 文件系统隔离

预期结果:
  - job A 写入的文件不应被 job B 看到
  - 共享文件系统在 job 间应完全隔离

验证点:
  - [负向] job A 在 /tmp 写入的文件，job B 不应能看到
  - [负向] job A 在 $HOME 写入的文件，job B 不应能看到

清理:      full_instance
