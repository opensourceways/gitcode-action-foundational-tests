用例 ID:   REL-FAULT-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-018
标题:      post 阶段 workflow 取消后仍执行 (run_always:true)

前置条件: workflow 含 post 阶段，step sleep 30，手动 cancel
操作步骤: 手动 cancel → 验证 post 阶段 step 日志可见
预期结果: post 正常执行完成；post 日志在 Run 详情可见
验证点: [正向] cancel 后 post 执行；[正向] post 日志可见
清理: none
