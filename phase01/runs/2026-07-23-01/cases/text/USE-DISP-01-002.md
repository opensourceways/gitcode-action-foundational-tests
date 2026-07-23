用例 ID:   USE-DISP-01-002
维度标签:   ['usability', 'completeness']
维度:      usability/completeness
优先级:    P1
溯源意图:  INTENT-USE-030
母意图:    —
标题:      workflow_dispatch 未提供参数但存在 default 时应使用默认值运行

前置条件:
  - workflow 配置了一个有 default 值的 input

操作步骤:
  1. 手动触发 workflow 不提供该参数

预期结果:
  workflow 使用默认值成功运行

验证点:
  - [正向] 运行成功完成
  - [正向] 日志中输出 default 值

清理:      无

