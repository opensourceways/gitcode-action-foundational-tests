用例 ID:   REL-RERUN-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-025
标题:      Re-run failed jobs：仅失败 job 重执行，成功 job 保留

前置条件: job A success, job B failure
操作步骤: Re-run failed → 仅 B 重执行，A cached
预期结果: B 重新执行；A 保留原结果不重执行
验证点: [正向] B 重新执行；[负向] A 不重执行
清理: none
