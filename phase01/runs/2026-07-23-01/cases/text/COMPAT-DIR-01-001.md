用例 ID:   COMPAT-DIR-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-029
母意图:    —
标题:      工作流目录差异——.gitcode/workflows/ 正常识别

前置条件:
  - 仓库已创建 .gitcode/workflows/ 目录

操作步骤:
  1. 在 .gitcode/workflows/ci.yml 中创建工作流定义
  2. 提交并推送到仓库
  3. 触发对应事件，验证工作流被正确识别和执行

预期结果:
  - .gitcode/workflows/ 下的 .yml 文件被平台识别为有效工作流
  - 对应事件触发时工作流正常执行
  - 此行为与 GitCode 官方文档一致

验证点:
  - [正向] .gitcode/workflows/*.yml 被正确识别
  - [正向] 对应事件触发后工作流正常执行
  - [负向] 不应出现 .gitcode 目录下文件被忽略的情况

清理:      fixture
