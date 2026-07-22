用例 ID:   SEC-RUNNER-LEAK-02-001
维度标签:   [security, reliability]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-025
母意图:    —
标题:      Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理）

前置条件:
  - runner 支持多 job 复用
  - 前一个 job 写入了敏感文件与环境变量

操作步骤:
  1. job-1 在 workspace 与 /tmp 写入标记文件与 secret
  2. job-2 在相同 runner 上检查 workspace 与 /tmp 是否存在 job-1 残留
  3. job-2 检查环境变量中是否残留 job-1 的 secrets

预期结果:
  - job-2 不应发现 job-1 的文件残留
  - 环境变量不应包含 job-1 的 secret 值

验证点:
  - [负向] job-2 日志不含 job-1 的 secret 明文
  - [负向] job-2 检查不到 job-1 的标记文件

清理:      重置 fixture 仓库
