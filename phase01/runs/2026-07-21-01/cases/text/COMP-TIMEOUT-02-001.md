用例 ID:   COMP-TIMEOUT-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-024
标题:      验证 timeout-minutes 超时终止与 job 状态标记

前置条件:
  - job 配置 timeout-minutes: 5

操作步骤:
  1. step 布置 sleep 600，job timeout-minutes: 5
  2. 验证超时终止 → job status = cancelled
  3. 日志含明确超时原因
  4. step timeout-minutes: 2 超时 → step 标记失败

预期结果:
  - 超时后 job 被强制终止
  - 状态为 cancelled（非 success）
  - 日志含超时标记

验证点:
  - [正向] job 超时终止 → cancelled
  - [正向] step 超时 → 失败
  - [正向] 日志含超时原因
  - [非功能] runner 正常回收

清理:      fixture
