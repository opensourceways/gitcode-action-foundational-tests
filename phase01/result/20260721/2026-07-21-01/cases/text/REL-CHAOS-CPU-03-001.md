用例 ID:   REL-CHAOS-CPU-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-015
标题:      CPU 饱和下 job 仍能推进且不被 OOM killer 误杀

前置条件:
  - step 执行 CPU 满载操作（使用 stress 或等效工具）

操作步骤:
  1. step 启动 CPU 满载进程（stress --cpu 4 --timeout 120s）
  2. CPU 满载期间执行后续 step
  3. 观察 job 是否正常完成（虽慢但执行到底）

预期结果:
  - job 在 timeout-minutes 内完成
  - 不被系统误 kill（status != cancelled/failure due to OOM）
  - 日志持续写入证明 liveness

验证点:
  - [正向] job 在 timeout 内完成
  - [正向] 日志持续产生
  - [负向] job 不因 CPU 饱和被系统 kill

清理:      none
