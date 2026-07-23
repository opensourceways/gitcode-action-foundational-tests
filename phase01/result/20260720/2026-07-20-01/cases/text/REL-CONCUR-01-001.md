用例 ID:   REL-CONCUR-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-001
标题:      高频 push 触发洪泛时排队与执行行为可预测

前置条件: 仓库 workflow 由 push 触发
操作步骤:
  1. 10s 内连续 push 20 次
  2. 验证 20 次触发全部产生 Run ID
  3. 验证 Run 按 FIFO 顺序排队
  4. 验证无 Run 被静默丢弃

预期结果: 20 次触发全产生 Run；按触发时间排队；无丢 Run
验证点:
  - [正向] 所有 Run ID 可枚举且 run_number 连续
  - [负向] 无 Run 被静默丢弃
清理:      none
