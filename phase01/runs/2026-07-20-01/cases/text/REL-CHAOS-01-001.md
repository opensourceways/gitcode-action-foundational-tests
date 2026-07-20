用例 ID:   REL-CHAOS-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P0
溯源意图:  INTENT-REL-015
母意图:    —
标题:      在 job 执行过程中 kill runner 进程，依赖该 job 的下游 job 应在超时后标记为失败，且被 kill 的 job 可重新运行恢复

前置条件:
  - 仓库支持 needs 依赖链（A→B）
  - 具备 runner 进程管理权限（可发送 SIGKILL）
  - 工作流含两个 job：job A（长运行步骤）+ job B（needs [A]）

操作步骤:
  1. 提交 workflow，配置 job A 执行 sleep 600（留时间窗口做 fault injection），job B needs [A]
  2. 触发 workflow，等 job A 进入 in_progress 后约 10s
  3. 对 runner 上的 runner agent 进程发送 SIGKILL
  4. 观察调度器对 job A 的处理：心跳超时后将 job A 标记为 failure 或 cancelled
  5. 观察 job B 的状态：因 job A 失败，job B 应被 skipped
  6. 执行 Re-run failed jobs，观察 job A 是否在新 runner 上成功完成

预期结果:
  - runner 被 kill 后，调度器在心跳超时（推定 60-180s）内将 job A 标记为 failure/cancelled
  - job A 不应永久保持 in_progress 状态（300s 内必须到达终态）
  - needs 依赖 job A 的 job B 被 skipped
  - Re-run failed jobs 后，job A 在干净 runner 上重新执行成功
  - 整个 workflow 最终状态为 success

验证点:
  - [正向] job A 在 180s 内到达 failure/cancelled 终态
  - [负向] job A 不应永久保持 in_progress（>300s）
  - [正向] job B 状态为 skipped（因 job A 失败）
  - [正向] Re-run failed jobs 后 job A 重新执行成功
  - [正向] Re-run 后整个 workflow 终态为 success

清理:      full_instance
