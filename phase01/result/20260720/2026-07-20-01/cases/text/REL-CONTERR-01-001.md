用例 ID:   REL-CONTERR-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-028
标题:      continue-on-error job 失败不阻断 workflow，默认依赖被 skipped

前置条件: A(continue-on-error,exit1), B(needs[A]), C(needs[A],if:always())
操作步骤: A failure → workflow 继续 → B skipped → C success
预期结果: A failure；B skipped；C success；A.result=failure
验证点: [正向] workflow 继续；[正向] B skipped；[正向] C success
清理: none
