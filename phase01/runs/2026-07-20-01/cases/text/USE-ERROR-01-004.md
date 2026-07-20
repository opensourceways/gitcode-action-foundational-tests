用例 ID:   USE-ERROR-01-004
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-004
标题:      触发器 types 取值无效时的错误信息可诊断性

前置条件: pull_request.types: [opened]（GitHub 命名）
操作步骤: 提交含非法 types → 记录报错 → 验证合法值列表
预期结果: 报错含无效值名 + 合法值列表 + 文件位置
验证点: [非功能] 消息含无效值+合法列表+位置
清理: fixture
