用例 ID:   USE-DEBUG-02-004
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-013
标题:      运行详情页 post 阶段的展示与文档一致性

前置条件:
  - workflow 带 post 阶段，主流程成功、post 故意失败

操作步骤:
  1. 触发包含 post 的 workflow
  2. 主流程成功结束后，观察 post 阶段在详情页中的展示
  3. 观察 post 失败时是否影响主 workflow 状态

预期结果:
  - post 有独立的展示区域，标注 "post" 或 "后处理"
  - post 失败不标记主 workflow 为 failure

验证点:
  - [正向] post 有独立展示区域
  - [正向] 标注 "post"/"后处理"
  - [非功能] UI 呈现直观

可理解性判据: eval: llm_assisted
清理:      fixture
