用例 ID:   USE-ERROR-01-003
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-003
标题:      未知字段/不支持属性时的错误信息可诊断性

前置条件: YAML 添加 GitCode 不支持的字段（如 container.credentials）
操作步骤: 提交 → 观察报错/warning → 若静默忽略需有警告
预期结果: 报错或 warning 指明字段不被支持 + 字段路径 + 建议查 GitCode 文档
验证点: [非功能] 有可见提示；[非功能] 消息指出 GitCode 差异
清理: fixture
