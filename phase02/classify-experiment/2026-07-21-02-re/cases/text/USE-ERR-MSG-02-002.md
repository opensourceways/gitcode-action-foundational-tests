用例 ID:   USE-ERR-MSG-02-002
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-004
标题:      触发器 types 取值无效时的错误信息可诊断性

前置条件:
  - 配置 pull_request.types 含 GitHub 命名值

操作步骤:
  1. types: [opened] → 验证报错含非法值 + 合法值列表
  2. types: [synchronize] → 同上
  3. types: [invalid_value] → 同上

预期结果:
  - 报错含指定非法值名、合法值列表、文件位置

验证点:
  - [正向] 非法值被点名
  - [正向] 合法值列表给出
  - [非功能] 消息可诊断: eval=llm_assisted

清理:      fixture
