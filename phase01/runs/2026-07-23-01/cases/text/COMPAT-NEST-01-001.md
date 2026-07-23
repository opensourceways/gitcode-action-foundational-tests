用例 ID:   COMPAT-NEST-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-015
母意图:    —
标题:      workflow_call 嵌套层数 - 2 层正常执行

前置条件:
  - 仓库已启用 Actions
  - 存在可复用的被调用 workflow 文件（2 层嵌套结构）

操作步骤:
  1. 在顶层 workflow 中使用 uses 调用第 2 层 workflow
  2. 提交并推送该 workflow
  3. 触发 workflow 并观察执行结果

预期结果:
  - 2 层 workflow_call 嵌套应正常执行
  - 运行状态应为成功

验证点:
  - [正向] 2 层嵌套 workflow 能正常触发并执行
  - [正向] 运行状态为成功

清理:      fixture
