用例 ID:   USE-RUN-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-006
母意图:    —
标题:      使用三段式标签时 job 正常调度

前置条件:
  - 仓库有可用的 dedicate-hosted runner

操作步骤:
  1. 使用 runs-on: [dedicate-hosted, x64, large]

预期结果:
  job 被成功调度到匹配的 runner

验证点:
  - [正向] 运行成功完成
  - [正向] job 日志显示在对应 runner 上执行

清理:      无

