用例 ID:   REL-RERUN-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-026
标题:      第 4 次 Re-run 被拒绝（最大 3 次）

前置条件: 一个必然失败的 workflow Run，连续触发 4 次 Re-run
操作步骤: 前 3 次 Re-run 正常 → 第 4 次被拒绝
预期结果: 第 4 次被拒绝，UI 按钮禁用或 API 返回错误
验证点: [正向] 前 3 次允许；[负向] 第 4 次拒绝
清理: none
