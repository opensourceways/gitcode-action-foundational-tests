用例 ID:   COMP-TRIG-01-075
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-237~430
母意图:    —
标题:      schedule 事件关键字段与 cron 格式验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 配置 schedule 触发并定义 cron 表达式
  2. 验证数组格式和字段访问

预期结果:
  - schedule 必须为数组格式 [{cron: ...}]，cron 五段式正确，atomgit.event.schedule 可访问

验证点:
  - [正向] 数组格式 schedule 通过校验
  - [负向] 对象格式 schedule 被拒绝
  - [正向] event.schedule 非空

清理:      重置 fixture 仓库
