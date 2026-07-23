用例 ID:   USE-INPT-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-008
母意图:    —
标题:      使用 string 类型 input 时正常通过校验

前置条件:
  - workflow 文件合法

操作步骤:
  1. 声明 workflow_dispatch inputs 的 type: string

预期结果:
  YAML 校验通过，可手动触发

验证点:
  - [正向] 运行可手动触发
  - [正向] 输入参数正常传递

清理:      无

