用例 ID:   COMP-RUNNER-EPH-03-001
维度标签:   [completeness, reliability, security]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-013
标题:      Runner 是否 ephemeral：验证托管 Runner 每次 job 分配全新实例还是可复用

前置条件:
  - 同一 workflow 连续两次 push 触发

操作步骤:
  1. 第一次 run：在 /tmp 写入标记文件 test-marker-$(date +%s)
  2. 第二次 run：检查 /tmp 是否存在上次的标记文件
  3. 检查环境变量、进程残留

预期结果:
  - 托管 Runner 应为 ephemeral（每次新实例）
  - 首次写入的标记文件不应在第二次 run 中存在
  - 若可复用：残留风险需记录为已知差异

验证点:
  - [正向] 两次 run 之间工作区独立
  - [正向] 前次 run 的 /tmp 文件不在后次 run 可见

清理:      fixture
