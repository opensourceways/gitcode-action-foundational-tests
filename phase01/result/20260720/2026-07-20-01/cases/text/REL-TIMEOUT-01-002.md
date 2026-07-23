用例 ID:   REL-TIMEOUT-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-010
标题:      多 job 独立超时时钟互不影响

前置条件: job A timeout=5, job B timeout=360；无 needs 依赖
操作步骤: job A sleep 600 → 超时终止；job B echo done → 正常成功
预期结果: A 超时 cancelled，B 正常 success；A 超时不触发 B 取消
验证点: [正向] B 不受 A 超时影响；[正向] A 在 5min 终止
清理: fixture
