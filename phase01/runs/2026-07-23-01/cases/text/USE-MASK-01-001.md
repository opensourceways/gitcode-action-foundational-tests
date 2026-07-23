用例 ID:   USE-MASK-01-001
维度标签:   ['usability', 'security']
维度:      usability/security
优先级:    P0
溯源意图:  INTENT-USE-016
母意图:    —
标题:      secret 脱敏文档描述与实际行为一致并给出缓解建议

前置条件:
  - 仓库配置了 TEST_SECRET

操作步骤:
  1. 在 workflow 中通过环境变量注入方式引用 secret
  2. 检查日志脱敏效果

预期结果:
  日志中 secret 显示为 ***；文档若声明绕过风险，必须同时给出正确写法示例

验证点:
  - [正向] 正常引用 secrets 时日志显示为 ***
  - [非功能] 文档中的风险提示段落是否包含如何改的可操作建议

清理:      无

