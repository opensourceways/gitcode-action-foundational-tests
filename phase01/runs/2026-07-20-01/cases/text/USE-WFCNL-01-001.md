用例 ID:   USE-WFCNL-01-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-022
标题:      `workflow_call` 嵌套超过 2 层时的错误信息可诊断性

前置条件:
  - GitCode 限制 workflow_call 最多嵌套 2 层
  - GitHub 无此硬限制

操作步骤:
  1. 构造三层 workflow_call 链：A → B → C（A 调用可重用 B，B 调用可重用 C）
  2. 触发 A，观察 C 的调用失败时的报错信息
  3. 验证报错是否明确指出：(a) 嵌套层级限制为 2 层，(b) 哪个调用超出限制，(c) 建议合并层级或改为直接调用

预期结果:
  - 报错应明确指出超过最大嵌套层级 2
  - 不应用泛化的 "workflow call failed" 让用户无从排查

验证点:
  - [正-非功能] 报错含 '2'（最大层级）和 'nest'/'level' 等关键词
  - [非功能] 消息是否让用户意识到需精简层级而非怀疑是 bug（0=看不出原因, 1=需查文档, 2=消息直接说明限制）

清理:      fixture
