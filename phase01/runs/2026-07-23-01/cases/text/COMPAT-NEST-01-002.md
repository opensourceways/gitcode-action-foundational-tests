用例 ID:   COMPAT-NEST-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-015
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    COMPAT-NEST-01-001
标题:      workflow_call 嵌套层数 - 3 层越界应报错

前置条件:
  - 仓库已启用 Actions
  - 存在可复用的被调用 workflow 文件（3 层嵌套结构）

操作步骤:
  1. 在顶层 workflow 中使用 uses 调用第 2 层 workflow
  2. 第 2 层 workflow 继续调用第 3 层 workflow
  3. 提交并推送该 workflow
  4. 观察平台校验或运行时行为

预期结果:
  - 平台应对超过 2 层的嵌套给出明确的校验错误或运行时错误
  - 错误信息应说明 workflow_call 最多支持 2 层嵌套

验证点:
  - [负向] 3 层嵌套不应被静默接受
  - [正向] 错误信息应明确指出嵌套层数限制

清理:      fixture
