用例 ID:   REL-TIMEOUT-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-011
标题:      timeout-minutes=0 非法值被配置校验拒绝

前置条件: workflow 含 timeout-minutes: 0
操作步骤: 提交 workflow → 验证解析/保存阶段报错拒绝
预期结果: 系统拒绝无效 timeout 值；无 job 被调度
验证点: [负向] timeout=0 被拒绝；[负向] 无 job 被调度
清理: fixture
