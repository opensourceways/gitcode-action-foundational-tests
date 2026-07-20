用例 ID:   REL-CHAOS-KILL-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-012
标题:      job 执行中被 kill runner 后 Run 状态正确标记为 failure

前置条件:
  - 1 个 job running（sleep 600s），kill runner 进程

操作步骤:
  1. 启动长时间运行的 job（sleep 600s）
  2. job 运行 30s 后 kill runner 进程（SIGKILL）
  3. 观察 Run 状态变化时间线

预期结果:
  - runner 失联后调度器在心跳超时内（≤5min）将 Run 标记为 failure
  - 被释放的 runner slot 可被排队中的下一个 job 使用
  - Run 日志中应有「runner disconnected」或等价提示

验证点:
  - [正向] kill 后 ≤5min Run 状态变为 failure
  - [正向] 释放的 runner slot 可被后续 job 使用
  - [负向] Run 不永久停留在 in_progress

清理:      full_instance
