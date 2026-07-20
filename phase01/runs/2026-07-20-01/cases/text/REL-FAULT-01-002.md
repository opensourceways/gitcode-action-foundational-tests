用例 ID:   REL-FAULT-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-017
标题:      runner 在 checkout 前崩溃 → 重运行后恢复

前置条件: job 启动后 5s 内 kill runner
操作步骤: kill runner → job 心跳超时 → Re-run all jobs 成功
预期结果: job 到达 failure/cancelled；Re-run all 全部 success
验证点: [正向] 心跳超时后 job 有终态；[正向] Re-run all 全部成功
清理: full_instance
