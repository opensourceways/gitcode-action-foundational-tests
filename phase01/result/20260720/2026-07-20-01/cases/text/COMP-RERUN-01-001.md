用例 ID:   COMP-RERUN-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-020
标题:      验证重运行机制：re-run all / re-run failed 的隔离性与状态保持

前置条件:
  - 仓库有多 job workflow（job A 成功，job B 故意失败）
  - workflow 配置了 stages 结构

操作步骤:
  1. 触发 workflow → job A success, job B failure
  2. 执行 Re-run failed jobs → 仅 job B 重执行，job A 保持 cached
  3. 修改 workflow 文件后执行 Re-run all jobs → 使用原始 commit 的配置
  4. 验证第 4 次重运行被拒绝（最大 3 次）
  5. 验证运行超过 6 小时的 run 无法重运行

预期结果:
  - Re-run failed → 仅失败 job 执行，成功 job 保持 cached
  - Re-run all → 所有 job 重新执行，run_number 递增
  - 重运行使用原始 commit 的配置（不读最新配置）
  - atomgit.sha/ref/event_name 保持原值
  - 第 4 次重运行被拒绝
  - 长时间运行（>6h）不可重运行

验证点:
  - [正向] Re-run failed 仅重跑失败 job
  - [正向] Re-run all 全部重跑，run_number 递增
  - [正向] 重运行使用原始配置
  - [负向] 超过 3 次重运行被拒绝
  - [负向] >6h 运行不可重运行

清理:      fixture
