用例 ID:   REL-RES-OOM-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-040
标题:      slim runner (1核4GB) 上执行 >4GB 内存任务时的 OOM 行为

前置条件:
  - 使用 slim flavor runner (1核4GB)
  - step 执行内存超限操作

操作步骤:
  1. 配置 runs-on=[ubuntu-latest, x64, slim]
  2. step 执行需要 >4GB 内存的操作
  3. 观察 job 是被 OOM kill 还是 hang

预期结果:
  - 超内存 job 被 OOM kill 后 Run = failure
  - 日志含 OOM/memory 错误
  - job 不无限 hang

验证点:
  - [正向] Run = failure
  - [正向] 日志含 OOM 或 memory 相关错误
  - [负向] job 不无限 hang

清理:      fixture
