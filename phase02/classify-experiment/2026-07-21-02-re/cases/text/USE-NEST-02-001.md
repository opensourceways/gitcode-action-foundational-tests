用例 ID:   USE-NEST-02-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-022
标题:      workflow_call 嵌套超过 2 层时的错误信息可诊断性

前置条件:
  - 构造 A → B → C 三层 workflow_call 链
  - GitCode 限制最多嵌套 2 层

操作步骤:
  1. 触发 A（call B → call C），验证 C 调用失败时的报错信息
  2. 验证错误消息是否明确指出：
     (1) 嵌套层级限制为 2 层
     (2) 哪个 workflow 调用超限
     (3) 建议合并层级或改为直接调用

预期结果:
  - 超限明确报错
  - 错误信息含 '2'（最大层级）+ 'nest'/'level' 等关键词

验证点:
  - [正向] 第 3 层调用被明确报错
  - [正向] 消息含层级限制和超限位置
  - [非功能] 消息能否让用户意识到需精简层级

可理解性判据: eval: llm_assisted
清理:      fixture
