用例 ID:   USE-DOC-02-002
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-008
标题:      文档声明的 environment 绑定语法与实际校验行为的一致性（复测 TC-010）

前置条件:
  - 文档描述了环境级 secret 审批功能
  - 已知 TC-010：environment 字段被平台报 "unknown property"

操作步骤:
  1. 按文档示例配置 `jobs.<id>.environment`
  2. 验证平台是否接受该字段（不报 "unknown property"）
  3. 若平台仍不接受：文档必须在对应处明确标注能力状态

预期结果:
  - 文档声明的能力有对应合法语法被平台接受
  - 或文档标注 "规划中/暂不支持"

验证点:
  - [正向] 平台接受或文档标明状态
  - [负向] 不应文档说可用但平台不接受

可理解性判据: eval: llm_assisted
清理:      fixture
