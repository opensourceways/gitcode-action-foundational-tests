用例 ID:   REL-FAULT-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-016
标题:      step 运行中网络不可用 60s → step 失败但后续恢复

前置条件: step curl 外部 URL，注入网络 drop 60s
操作步骤: 网络不可用期间 curl 失败 → 网络恢复后 if:always() step 正常
预期结果: curl step 失败；后续恢复后 step 正常；job 终态正确
验证点: [正向] step 失败非零退出；[正向] 后续 step 正常；[正向] job failure
清理: fixture
