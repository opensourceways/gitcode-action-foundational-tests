用例 ID:   REL-ARTIFACT-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-029
标题:      artifact 上传中 workflow 取消 → artifact 不可下载

前置条件: workflow 上传 100MB artifact + sleep 30，上传中 cancel
操作步骤: cancel → artifact 标记 incomplete → 后续 Run 无法下载
预期结果: 被取消 Run 的 artifact 不可下载；下载报错
验证点: [负向] 后续 Run 不下载损坏 artifact；[正向] 错误信息可操作
清理: none
