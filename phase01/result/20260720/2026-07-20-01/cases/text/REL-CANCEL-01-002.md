用例 ID:   REL-CANCEL-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-020
标题:      stages.fail_fast=true 时首 job 失败同 stage 其余被取消

前置条件: 2-stage workflow，stage1 job A 快失败 + job B sleep 120
操作步骤: job A exit 1 → job B cancelled → stage2 skipped → workflow failure
预期结果: B cancelled；后续 stage skipped；workflow 终态 failure
验证点: [正向] B cancelled；[正向] 后续 stage skipped；[正向] workflow failure
清理: none
