用例 ID:   COMPAT-UNSUPP-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
标题:      验证不支持特征的降级行为不静默忽略
incorporates: TC-010 (environment 字段), TC-273 (container.image)

前置条件:
  - 使用 GitCode 不支持但 GitHub 支持的字段

操作步骤:
  1. jobs.<id>.environment → 验证报错（TC-010 已确认报 unknown property）
  2. jobs.<id>.container.image → 验证报错（非静默）
  3. runs.using: node20/docker/composite → 验证报错
  4. jobs.<id>.services → 验证报错

预期结果:
  - 不支持的特征应报错
  - 安全相关的绝不可静默忽略

验证点:
  - [正向] 不支持字段报错
  - [负向] 无静默忽略
  - [正向] 报错含字段路径

清理:      fixture
