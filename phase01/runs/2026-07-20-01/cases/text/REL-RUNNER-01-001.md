用例 ID:   REL-RUNNER-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-012
标题:      step 超过 runner 内存上限 → OOM kill → job failure

前置条件: small runner (2C/8G)，step 逐步分配超 8GB 内存
操作步骤: step 分配超限内存 → 进程被 OOM kill (exit 137)
预期结果: job status = failure；runner 继续存活
验证点: [正向] exit code 非零；[正向] runner 不崩溃
清理: fixture
