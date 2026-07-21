用例 ID:   REL-TIMEOUT-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-009
标题:      job timeout-minutes=5 时超过 5 分钟的 step 被强制终止

前置条件:
  - job timeout-minutes=5, step sleep 600

操作步骤:
  1. 启动后计时
  2. 验证 5min ± 30s 内 job 被终止
  3. 日志含超时标记
  4. runner 被正常回收

预期结果:
  - job 在 5min ± 30s 内终止
  - 状态为 cancelled
  - 日志含超时原因

验证点:
  - [正向] 5min 内终止
  - [正向] 日志含 timeout 标记
  - [负向] 不持续运行 > 10min
  - [非功能] runner 正常回收

清理:      fixture
