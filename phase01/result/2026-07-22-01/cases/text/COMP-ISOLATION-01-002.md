用例 ID:   COMP-ISOLATION-01-002
维度标签:   [completeness]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-011
母意图:    —
标题:      跨 job 的 Runner 文件系统隔离应有效

前置条件:
  - 仓库已启用 Actions
  - 使用平台托管 Runner

操作步骤:
  1. 触发一个包含两个 job 的 workflow
  2. job-a 在 /tmp 目录写入隔离标记文件
  3. job-b 在 job-a 完成后，检查 /tmp 目录是否存在该标记

预期结果:
  - job-b 不应读取到 job-a 写入的标记文件
  - 即使两 job 被调度到同一物理 Runner，环境也应被清理或隔离

验证点:
  - [正向] job-b 日志显示 ISOLATION_STRONG: marker not visible across jobs
  - [负向] job-b 日志不含 ISOLATION_WEAK

清理:      重置 fixture 仓库
