用例 ID:   COMPAT-MISSFN-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-010
母意图:    —
标题:      缺失表达式函数 join() / fromJSON() / case() 的降级行为

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中尝试使用 GitHub 存在的表达式函数 `join()`、`fromJSON()`、`case()`
  2. 提交并推送该 workflow
  3. 观察平台解析行为：是报错拒绝、静默忽略还是部分支持

预期结果:
  - 平台对不支持的表达式函数给出明确的 YAML 校验错误或运行时错误
  - 错误信息应指明该函数在 GitCode 中不可用，而非 generic 语法错误
  - 不应出现静默求值错误结果（如空值、意外字符串）

验证点:
  - [负向] 不支持函数不应静默通过并返回意外值
  - [正向] 错误信息应足够清晰，帮助迁移者识别函数缺失

清理:      fixture
