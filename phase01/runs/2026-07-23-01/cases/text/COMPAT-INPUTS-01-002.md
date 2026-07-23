用例 ID:   COMPAT-INPUTS-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-014
母意图:    COMPAT-INPUTS-01-001
标题:      workflow_dispatch inputs 类型限制 - string 正常通过

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 中定义 workflow_dispatch inputs 并指定 type: string
  2. 提交并推送该 workflow
  3. 触发 workflow 并传入参数

预期结果:
  - workflow 应被平台接受，不报错
  - string 类型的 input 应能正常接收和输出

验证点:
  - [正向] workflow 校验通过
  - [正向] string 类型 input 能正常传递和使用

清理:      fixture
