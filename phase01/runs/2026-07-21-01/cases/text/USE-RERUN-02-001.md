用例 ID:   USE-RERUN-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-020
标题:      Re-run failed jobs 后成功 job 的结果和日志保留与展示

前置条件:
  - 多 job workflow：job A 成功，job B 失败
  - Re-run failed jobs

操作步骤:
  1. 首次运行：job A success，job B 故意失败
  2. Re-run failed jobs
  3. 验证新 run 中 job A 显示 cached/passed 且日志可查
  4. 验证原始 run 日志完整

预期结果:
  - 成功 job 标注 cached/已缓存/已通过
  - 原始日志可展开查看
  - job A 不被重新执行

验证点:
  - [正向] job A 显示 cached 且日志可查
  - [正向] 原始 run 日志完整
  - [负向] job A 不被隐式重新执行

清理:      fixture
