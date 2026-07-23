用例 ID:   REL-SCHED-01-010
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-057
母意图:    —
标题:      资源调度状态一致性——空闲 runner 存在时 job 不应死等

前置条件:
  - 仓库已启用 Actions
  - 有至少 1 个处于 idle 状态的 runner 与该仓库匹配
  - 无其他正在运行的 job 占用该 runner

操作步骤:
  1. 确认 runner 列表中存在 idle 状态 runner（通过 API 查询）
  2. 创建单 job workflow，指定 `runs-on` 标签与 idle runner 匹配
  3. 触发 workflow 运行
  4. 持续监控 job 状态变化与 runner 状态变化

预期结果:
  - job 应在合理时间内（≤ 30 秒）从 queued 转为 running
  - idle runner 应在 job 启动后转为 busy 状态
  - job 不应长时间 stuck 在 queued（无 runner 分配）

验证点:
  - [正向] queued→running 时间 ≤ 30 秒
  - [正向] runner 状态从 idle 转为 busy
  - [负向] job 不卡在 queued 超过 60 秒

清理:      重置 fixture 仓库
