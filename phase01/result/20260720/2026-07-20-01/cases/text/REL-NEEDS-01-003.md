用例 ID:   REL-NEEDS-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-023
标题:      fan-in 汇聚：C 依赖 A 和 B，A success 但 B failure → C skipped

前置条件: A(success), B(exit 1), C(needs:[A,B])
操作步骤: A success + B failure → C skipped，不为 success
预期结果: C skipped；A success 保持
验证点: [正向] C skipped；[负向] C 不为 success
清理: none
