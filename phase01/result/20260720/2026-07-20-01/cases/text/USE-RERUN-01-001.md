用例 ID:   USE-RERUN-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-020
标题:      Re-run failed jobs 后成功 job 的结果和日志保留与展示

前置条件:
  - 配置一个多 job workflow（job A 成功 + job B 失败）
  - `rerun-failed-jobs.md` 声称成功 job 日志在新 run 中保留

操作步骤:
  1. 提交并运行多 job workflow，确认 job A 成功、job B 失败
  2. 执行 Re-run failed jobs
  3. 观察新 run 详情页中 job A 是否显示 "cached" / "已缓存" / "passed" / "已通过"
  4. 展开 job A 日志，验证原始日志可查看
  5. 回到原始 run，验证其日志仍然完整未被清除
  6. 确认 job A 未被隐式重新执行（即不消耗额外 Runner 资源）

预期结果:
  - 新 run 中成功 job 标注 "cached" / "已缓存" / "passed" / "已通过"
  - 成功 job 的日志可展开查看
  - 原始 run 日志未被清除
  - 成功 job 不被重新执行

验证点:
  - [正-非功能] job A 显示 cached/passed 状态（可截图判定）
  - [正-非功能] job A 日志可展开查看
  - [正-非功能] 原始 run 日志完整保留
  - [负向] 成功 job 不应被隐式重新执行

清理:      fixture
