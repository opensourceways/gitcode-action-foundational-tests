用例 ID:   COMP-TRIG-01-074
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-084~085
母意图:    —
标题:      workflow_dispatch 事件关键字段与 inputs 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 配置 workflow_dispatch 触发并定义 inputs 参数
  2. 手动触发并传入参数验证

预期结果:
  - workflow_dispatch 支持手动触发，inputs 参数仅支持 string 类型，default 和 required 生效，atomgit.event.inputs 可访问

验证点:
  - [正向] 手动触发成功创建 run
  - [正向] inputs 参数值在 step 中可访问
  - [正向] 未传参时使用 default 值

清理:      重置 fixture 仓库
