用例 ID:   SEC-RUN-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-021
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 环境变量与共享目录必须跨 job 隔离

前置条件:
  - 仓库支持多 job workflow

操作步骤:
  1. 提交一个多 job workflow，job A 设置环境变量和 /tmp 文件
  2. job B 检查环境变量和 /tmp 是否被污染

预期结果:
  - job B 的环境变量和共享目录在启动时为干净状态
  - job B 不应继承 job A 的设置

验证点:
  - [负向] job B 绝不应继承到 job A 设置的环境变量或 /tmp 残留
  - [非功能] 自托管 runner 上应执行与官方 runner 同等级别的清理

清理:      重置 fixture 仓库
