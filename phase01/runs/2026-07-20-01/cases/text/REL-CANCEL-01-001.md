用例 ID:   REL-CANCEL-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-019
标题:      手动取消运行中 step → SIGTERM 终止 → 清理 step 仍执行

前置条件: step sleep 600, 手动 cancel
操作步骤: cancel → step 收到 SIGTERM，10s 内终止 → if:always() 清理 step 执行
预期结果: step 终止；清理 step 执行；job cancelled
验证点: [正向] step 10s 内终止；[正向] 清理 step 执行；[正向] job cancelled
清理: none
