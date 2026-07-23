用例 ID:   COMPAT-INPUTS-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-014
母意图:    —
标题:      workflow_dispatch inputs 类型限制 - boolean 应报错

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中定义 workflow_dispatch inputs 并指定 type: boolean
  2. 提交并推送该 workflow
  3. 观察平台校验行为

预期结果:
  - 平台应对不支持的 boolean 类型给出明确的校验错误
  - 错误信息应提示仅支持 string 类型

验证点:
  - [负向] boolean 类型不应被静默接受
  - [正向] 错误信息应明确指出仅支持 string 类型

清理:      fixture
