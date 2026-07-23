用例 ID:   REL-LATENCY-01-009
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-050
母意图:    —
标题:      调度延迟基准——queued 到 running 的 P50/P95 等待时间应满足基准

前置条件:
  - 仓库已启用 Actions
  - runner 资源处于正常负载状态（非饱和）
  - 具备 API 查询 job 状态与时间戳的能力

操作步骤:
  1. 创建简单的单 job workflow（运行时间 < 10 秒）
  2. 连续触发 20 次该 workflow（间隔 5 秒，避免人为洪泛）
  3. 通过 API 获取每次运行的 jobs 列表，提取 queued 时间和 running 时间
  4. 计算 20 次运行的 queued→running 延迟分布

预期结果:
  - P50 延迟 ≤ 15 秒（50% 的 job 在 15 秒内获得 runner）
  - P95 延迟 ≤ 45 秒（95% 的 job 在 45 秒内获得 runner）
  - 无任何 job 的等待时间超过 60 秒（在 runner 资源正常时）

验证点:
  - [非功能] P50 queued→running ≤ 15 秒
  - [非功能] P95 queued→running ≤ 45 秒
  - [负向] 无 job 等待 > 60 秒

清理:      重置 fixture 仓库
