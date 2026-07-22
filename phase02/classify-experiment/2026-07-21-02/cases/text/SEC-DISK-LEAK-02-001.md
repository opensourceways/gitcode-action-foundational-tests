用例 ID:   SEC-DISK-LEAK-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-026
母意图:    —
标题:      共享盘（/tmp、workspace）不跨 job 泄露敏感文件

前置条件:
  - job-A 在 /tmp 与 workspace 创建含敏感数据的文件

操作步骤:
  1. job-A 写入 /tmp/secret.txt 与 $GITHUB_WORKSPACE/secret.txt
  2. job-B 读取 /tmp/secret.txt 与 workspace/secret.txt

预期结果:
  - job-B 应读取不到 job-A 的敏感文件
  - 共享盘在 job 切换时应被清理或隔离

验证点:
  - [负向] job-B 日志不含 job-A 的敏感数据
  - [正向] job-B 报告文件不存在

清理:      重置 fixture 仓库
