用例 ID:   REL-CONV-02-001
维度标签:   [reliability, completeness]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-036
母意图:    —
标题:      schedule 触发收敛与取消语义——Scheduler 修复后调度运行可达终态

前置条件:
  - 仓库位于默认分支
  - Scheduler 已修复并可工作
  - 有可用的 runner 资源

操作步骤:
  1. 部署 schedule workflow，cron 配置为 `*/5 * * * *`
  2. job 内包含创建标记文件 step、sleep 180s step 及 post 清理步骤
  3. 在运行进入 running 后约 30s 执行手动 Cancel
  4. 观测 15min 内触发次数、取消后终态、post 清理执行与 runner 释放情况

预期结果:
  - 15min 内至少触发 1 次 schedule 运行
  - 计划时刻与实际 running 时刻差不超过 5min
  - 取消后运行终态收敛为 cancelled
  - post 清理步骤执行，标记文件被删除
  - 取消后 60s 内同 runner 可成功调度新探针 job

验证点:
  - [正向] 15min 内触发次数≥1，日志可查看，atomgit.event_name 为 schedule
  - [负向] 不应复现历史「cron 配置正确但运行历史永远空白」故障；取消后不应无限停留在 running，也不应错标为 success/failure
  - [非功能] 触发延迟≤5min；取消后 runner 在 60s 内释放并可调度新 job

清理:      重置 fixture 仓库
