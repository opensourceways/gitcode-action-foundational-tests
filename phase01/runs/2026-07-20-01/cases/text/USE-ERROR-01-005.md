用例 ID:   USE-ERROR-01-005
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-005
标题:      表达式语法差异（括号）的错误信息可诊断性

前置条件: if: ${{ failure() }}（GitHub 带括号语法）
操作步骤: 提交 → 记录报错 → 验证消息提示 GitCode 不需要括号
预期结果: 报错含表达式位置 + 提示用 failed 替代 failure()
验证点: [非功能] 消息让迁移者意识到 GitCode 不需要括号
清理: fixture
