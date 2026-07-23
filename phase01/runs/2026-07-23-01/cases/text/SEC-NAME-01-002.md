用例 ID:   SEC-NAME-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-025
母意图:    —
标题:      通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，执行 printenv 或读取 /proc/self/environ
  2. 触发 workflow 并查看运行日志

预期结果:
  - printenv 输出到日志时，secret 值必须被脱敏
  - 即使通过 env | grep 过滤，过滤后的值也应被脱敏

验证点:
  - [负向] printenv 输出到日志时，secret 值必须被脱敏，绝不应保留原值
  - [非功能] 即使通过 env | grep 过滤，过滤后的值也应被脱敏

清理:      重置 fixture 仓库
