用例 ID:   COMPAT-COMPOSITE-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-042
标题:      Composite Action 不支持：验证使用 composite action 时的报错质量——历史 #41

前置条件:
  - 创建 action.yml 使用 runs.using: composite
  - 在 workflow 中引用该 composite action

操作步骤:
  1. 创建 action.yml 含 runs.using: composite 和多个 steps
  2. 在 workflow 中通过 uses: ./ 引用该 composite action
  3. 触发 workflow 观察报错信息

预期结果:
  - 应明确报错：「composite action 暂不支持」（而非无日志失败）
  - 报错信息应给出替代方案（如使用 workflow_call）
  - 文档 actions-list 应标注 composite 不支持状态

验证点:
  - [正向] 使用 composite action 时明确报错
  - [正向] 报错含「composite」或「不支持」关键词
  - [负向] 不应失败无日志（历史 #41：任务失败且无报错信息）

清理:      fixture
