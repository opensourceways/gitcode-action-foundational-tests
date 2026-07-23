用例 ID:   COMPAT-EXPR-01-011
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-010
母意图:    —
标题:      join() 函数缺失时的降级行为

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow run 块中引用 GitHub 支持的 join() 表达式函数
  2. 提交并推送该 workflow
  3. 观察平台解析与运行行为

预期结果:
  - 平台对不支持的 join() 函数给出明确的校验错误或运行时错误
  - 错误信息应指明该函数在 GitCode 中不可用
  - 不应静默求值并返回意外结果

验证点:
  - [负向] 不支持函数不应静默通过并返回意外值
  - [正向] 错误信息应足够清晰，帮助迁移者识别函数缺失

清理:      fixture
