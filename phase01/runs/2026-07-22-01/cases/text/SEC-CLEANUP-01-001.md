用例 ID:   SEC-CLEANUP-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-020
母意图:    —
标题:      Job 结束后 workspace 与临时文件应被彻底清理

前置条件:
  - 仓库存在多 job workflow
  - Runner 支持连续执行多个 job

操作步骤:
  1. 提交一个 workflow，在第一个 job 中向 workspace 写入敏感临时文件（如 secret 副本、构建产物）
  2. 在第二个 job（同 runner 或后续 runner）中尝试读取前一个 job 的 workspace 路径
  3. 观察第二个 job 执行结果

预期结果:
  - 第二个 job 无法读取第一个 job 遗留的敏感文件
  - workspace 路径不存在或已被清空
  - 系统不跨 job 保留 workspace 内容

验证点:
  - [负向] 第二个 job 未读取到第一个 job 遗留的敏感文件
  - [负向] workspace 中不存在前序 job 的临时文件
  - [正向] 第二个 job 正常执行清理检查步骤

清理:      重置 fixture 仓库
