用例 ID:   COMPAT-UNSUP-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
标题:      不支持特征的降级行为：报错 vs 静默忽略

前置条件: 仓库 workflow 使用 GitCode 不支持的特征
操作步骤:
  1. environment 字段 → 验证报错（TC-010 已知）
  2. container.image → 验证报错而非静默忽略
  3. runs.using:node20 → 验证报错
  4. jobs.<id>.services → 验证报错
预期结果: 所有不支持特征明确报错，不静默忽略
验证点:
  - [正向] 不支持字段明确报错
  - [负向] 不应静默忽略任何不支持特征
清理:      fixture
