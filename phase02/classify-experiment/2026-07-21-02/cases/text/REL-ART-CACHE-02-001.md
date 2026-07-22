用例 ID:   REL-ART-CACHE-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-029
标题:      artifact 上传过程中 workflow 被取消，artifact 状态为 incomplete 且不污染后续下载

前置条件:
  - workflow 含大文件（100MB）上传 artifact 步骤 + 给取消留窗口的 sleep 30
  - 在上传期间手动取消

操作步骤:
  1. 触发包含大文件上传 + sleep 的 workflow
  2. 在上传到一半时手动 cancel
  3. 验证 artifact 不可被后续 Run 下载
  4. 验证错误信息包含可操作提示

预期结果:
  - 被取消 Run 的 artifact 不可下载
  - 后续 Run 不会使用损坏的 artifact

验证点:
  - [正向] artifact 不可下载
  - [负向] 后续 Run 不会使用损坏 artifact
  - [非功能] 错误信息含可操作提示

清理:      fixture
