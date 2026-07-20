用例 ID:   REL-TIMEOUT-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-009
标题:      timeout-minutes=5 超时强制终止 job

前置条件: job timeout-minutes=5，step sleep 600
操作步骤:
  1. 触发 workflow
  2. 验证 job 在 5min +/- 30s 内终止
  3. 验证 job 状态为 cancelled（非 success）
  4. 验证日志包含超时原因

预期结果: 超时后强制终止；状态正确标记；日志含原因
验证点:
  - [正向] 超时终止时间准确
  - [正向] job 状态为 cancelled
  - [正向] 日志含超时标记
清理:      fixture
