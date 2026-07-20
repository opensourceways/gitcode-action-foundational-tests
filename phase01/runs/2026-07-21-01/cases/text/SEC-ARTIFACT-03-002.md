用例 ID:   SEC-ARTIFACT-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-042
母意图:    —
标题:      workflow_run 事件下下载的 artifact 应被视为不可信输入

前置条件:
  - 存在 workflow_run 触发的工作流
  - 前置 workflow 上传了 artifact

操作步骤:
  1. workflow_run 触发的特权 workflow 下载前置 workflow 的 artifact
  2. 检查下载的 artifact 是否有来源标记
  3. 验证特权 workflow 是否有机制区分可信/不可信 artifact

预期结果:
  - 下载的 artifact 应有明确来源标记
  - 平台文档应警告 artifact 投毒风险

验证点:
  - [负向] 从其他 workflow 下载的 artifact 应标注来源信息
  - [正向] 若平台不支持 workflow_run，标记为 N/A

清理:      none
