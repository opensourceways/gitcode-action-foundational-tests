用例 ID:   COMP-TIMEOUT-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-024
标题:      验证 timeout-minutes 超时终止与 job 状态标记

前置条件:
  - 仓库有正常 workflow 配置
  - 默认 job 超时 360 分钟

操作步骤:
  1. 配置 job 设 timeout-minutes: 5，执行 sleep 600 → 验证超时终止
  2. 配置 step 设 timeout-minutes: 2 → 验证 step 超时终止
  3. 验证超时后 job 状态为 cancelled（非 success）
  4. 验证超时日志包含明确原因
  5. 不设 timeout 的 job 对比 → 不受影响

预期结果:
  - job timeout-minutes:5 → 5 分钟后被强制终止，状态 cancelled
  - step timeout-minutes:2 → 2 分钟后 step 被终止，标记失败
  - 超时日志含明确超时原因
  - 未设 timeout 的 job 不受短超时限制

验证点:
  - [正向] job 超时终止 → 状态 cancelled
  - [正向] step 超时终止 → step 失败 + 日志含原因
  - [正向] 未设 timeout 的 job 不受影响
  - [负向] 超时 job 不应标记为 success

清理:      fixture
