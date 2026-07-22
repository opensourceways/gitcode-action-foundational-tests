用例 ID:   REL-CONCUR-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-001
标题:      同一 workflow 10s 内被 push 连续触发 20 次，排队与执行行为可预测

前置条件:
  - 10s 窗口内连续 push 20 次触发同一 workflow

操作步骤:
  1. 所有 20 次触发均产生可追踪的 Run ID
  2. Run 按 FIFO 顺序进入执行
  3. 无 Run 被静默丢弃
  4. 第 1 次触发的 Run 在 120s 内进入 in_progress

预期结果:
  - 所有触发产生 Run
  - 按触发顺序执行
  - run_number 连续

验证点:
  - [正向] 所有 20 次产生 Run ID 可枚举
  - [正向] run_number 严格递增
  - [负向] 无 Run 被丢弃
  - [非功能] 首 Run < 120s 进入执行

清理:      fixture
