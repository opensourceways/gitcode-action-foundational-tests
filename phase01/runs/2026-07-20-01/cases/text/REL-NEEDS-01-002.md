用例 ID:   REL-NEEDS-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-022
标题:      needs 链 A→B→C 中 A 失败 → B/C skipped → D(always) 执行

前置条件: 4-job 链 A→B→C→D，A exit 1，D if:always()
操作步骤: A failure → B skipped → C skipped → D 正常执行
预期结果: B/C skipped；D success；B/C 不为 success
验证点: [正向] B/C skipped；[正向] D success；[负向] B/C 不为 success
清理: none
