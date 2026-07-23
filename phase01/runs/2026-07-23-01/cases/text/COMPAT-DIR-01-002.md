用例 ID:   COMPAT-DIR-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-029
母意图:    COMPAT-DIR-01-001
标题:      工作流目录差异——.github/workflows/ 不应被识别

前置条件:
  - 仓库已创建 .github/workflows/ 目录
  - 该目录下存在工作流定义文件

操作步骤:
  1. 在 .github/workflows/ci.yml 中创建工作流定义
  2. 同时确保 .gitcode/workflows/ 下无同名工作流
  3. 提交并推送到仓库，触发对应事件
  4. 观察平台是否识别并执行 .github/workflows/ 下的工作流

预期结果:
  - .github/workflows/ 下的工作流文件不被 GitCode 平台识别
  - 对应事件触发时，该目录下的工作流不会执行
  - 平台优先且仅识别 .gitcode/workflows/ 目录

验证点:
  - [负向] .github/workflows/ 下的工作流不应被触发执行
  - [正向] 平台应仅识别 .gitcode/workflows/ 目录
  - [正向] 事件触发后不应出现来自 .github 目录的意外运行记录

清理:      fixture
