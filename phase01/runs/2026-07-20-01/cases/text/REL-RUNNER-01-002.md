用例 ID:   REL-RUNNER-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-013
标题:      step 填充 runner 磁盘超 50GB → job failure

前置条件: small runner (50GB disk)，step dd 填充磁盘
操作步骤: dd 填充磁盘 → 写操作收到 ENOSPC → job failure
预期结果: job 失败；日志含 "No space left" 信息
验证点: [正向] exit code 非零；[正向] 日志含磁盘满信息
清理: fixture
