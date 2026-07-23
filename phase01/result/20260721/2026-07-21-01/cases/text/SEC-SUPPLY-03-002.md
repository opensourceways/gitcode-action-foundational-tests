用例 ID:   SEC-SUPPLY-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-030
母意图:    —
标题:      第三方 action 的输入参数中的不可信值不应导致 action 内部代码注入

前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题

操作步骤:
  1. 在 PR 标题中放入 shell 元字符
  2. workflow 将该标题作为 with 参数传给 action
  3. 观察 action 是否能正确处理含特殊字符的输入

预期结果:
  - 含 shell 元字符的 PR 标题作为 with 参数传入 action 时不应产生注入
  - action 内部应以纯数据处理 with 参数

验证点:
  - [负向] 含 shell 元字符的 PR 标题作为 with 参数传入 action 不应产生注入痕迹
  - [正向] 安全 JS/TS action 应正确处理含特殊字符的标题

清理:      fixture
