用例 ID:   REL-NEEDS-01-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-024
标题:      needs 指向 matrix 父 job 等待所有实例完成

前置条件: job A matrix(os=[ubuntu,ubuntu-22]) 2 实例，C needs[A]
操作步骤: C 在所有 matrix 实例完成后执行；验证无"任务初始化错误"
预期结果: C 等待全部实例；C 可访问 needs 上下文
验证点: [正向] C 等待完成；[负向] 无初始化错误（TC-486）
清理: none
