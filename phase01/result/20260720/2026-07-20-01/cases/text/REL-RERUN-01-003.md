用例 ID:   REL-RERUN-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-027
标题:      Re-run all 后 RUN_ID/RUN_NUMBER 更新，atomgit.sha 保持

前置条件: 触发一次 Run，Re-run all 一次
操作步骤: 比对两次 Run 的 run_id, run_number, atomgit.sha
预期结果: run_id 变化；run_number 递增；sha 保持不变
验证点: [正向] run_id != 旧值；[正向] run_number > 旧值；[正向] sha 相同
清理: none
