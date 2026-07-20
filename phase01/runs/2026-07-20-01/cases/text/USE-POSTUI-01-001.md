用例 ID:   USE-POSTUI-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-013
标题:      运行详情页 `post` 阶段的展示与文档一致性

前置条件:
  - 配置带 post 阶段的 workflow
  - post 默认 `run_always: true`

操作步骤:
  1. 提交带 post 的 workflow，故意让主流程成功、post 失败
  2. 观察运行详情页中 post 阶段的展示方式
  3. 验证 post 阶段是否与主 stages 有视觉区分（独立展示区域、标注 "post" 或 "后处理"）
  4. 验证 post 失败不标记主 workflow 为 failure

预期结果:
  - post 阶段应单独展示，标注 "post" 或 "后处理"
  - post 与正常 stage 不应混排
  - post 失败不应导致主 workflow 状态变为 failure

验证点:
  - [正-非功能] post 有独立展示区域（可截图判定）
  - [正-非功能] 标注文字含 "post" 或 "后处理"
  - [正-非功能] post 失败时主 workflow 状态仍为 success
  - [非功能] UI 呈现是否直观——用户能否一眼看出这是后处理（LLM 辅助评判）

清理:      fixture
