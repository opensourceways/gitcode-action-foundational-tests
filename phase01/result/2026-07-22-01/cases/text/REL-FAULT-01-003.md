用例 ID:   REL-FAULT-01-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-031
母意图:    —
标题:      故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

前置条件:
  - 仓库已启用 Actions
  - runner 正常运行且可被注入故障

操作步骤:
  1. 创建包含多步骤的 workflow（如生成日志文件、执行耗时操作）
  2. 触发 workflow 运行
  3. 在 job 执行过程中对 runner 进程注入 SIGKILL
  4. 等待系统处理并查看运行结果与日志

预期结果:
  - 该 job 的运行状态被记录为失败（FAILED）
  - SIGKILL 之前已执行步骤的日志被完整保留，可供下载查看
  - 未执行步骤不产生日志

验证点:
  - [正向] job 状态为 FAILED
  - [正向] 已执行步骤的日志可下载且内容完整
  - [负向] 日志中不出现未执行步骤的虚假成功记录

清理:      重置 full_instance
