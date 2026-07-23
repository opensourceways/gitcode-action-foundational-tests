用例 ID:   USE-ERROR-01-002
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-002
标题:      字段类型错误时的错误信息可诊断性

前置条件: 提交 runs-on 为 string（非 list）或 env 为 string（非 map）
操作步骤: runs-on: "ubuntu-latest" → 记录报错；env: "foo" → 记录报错
预期结果: 报错含字段路径、期望类型、实际类型、行号
验证点: [非功能] 消息含字段路径+期望类型+实际类型+行号
清理: fixture
