用例 ID:   USE-DOCENV-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-008
标题:      文档声明的 `environment` 绑定语法与实际校验行为的一致性

前置条件:
  - 现有案例 TC-010 已知：`environment` 字段报 "unknown property"
  - 文档 `using-secrets.md` 描述了环境级 secret 审批功能

操作步骤:
  1. 按文档示例配置 `jobs.<id>.environment` 字段
  2. 提交 workflow，触发 push
  3. 观察平台是否接受该字段（不报 "unknown property"）
  4. 若平台仍报错，检查文档该处是否标注「规划中」或「暂不支持」

预期结果:
  - 若能力已实现：平台应接受 `environment` 字段
  - 若能力未实现：文档必须在对应位置明确标注能力状态（规划中 / 暂不支持）

验证点:
  - [正-非功能] 平台是否接受文档示例中的 environment 字段（可观测）
  - [非功能] 若文档-行为不一致，文档必须有状态标注

清理:      fixture
