用例 ID:   COMP-RERUN-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-020
标题:      验证重运行机制 re-run all / re-run failed 的隔离性与状态保持

前置条件:
  - workflow 含 jobA（成功）+ jobB（失败）

操作步骤:
  1. Re-run all jobs → 所有 job 重新执行，run_number 递增
  2. Re-run failed jobs → 仅 jobB 重新执行，jobA 保持 cached
  3. 修改 workflow 文件后 re-run → 使用原始 commit 配置
  4. 超过 360min 的 run 不可 re-run

预期结果:
  - Re-run all 使用原始配置
  - Re-run failed 仅跑失败 job
  - atomgit.sha/ref/event_name 保持原值

验证点:
  - [正向] Re-run all 全部重执行
  - [正向] Re-run failed 仅失败 job 执行
  - [正向] 使用原始配置
  - [负向] 超时 > 360min 的 run 不可重跑

清理:      fixture
