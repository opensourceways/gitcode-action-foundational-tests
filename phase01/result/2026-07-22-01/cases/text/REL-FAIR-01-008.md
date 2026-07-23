用例 ID:   REL-FAIR-01-008
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-044
母意图:    —
标题:      并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度

前置条件:
  - 仓库已启用 Actions
  - 至少具备 3 个可用 runner（使并发竞争有意义）

操作步骤:
  1. 创建 workflow A，包含 3 个独立 job（A1, A2, A3），每个运行约 30 秒
  2. 创建 workflow B，包含 3 个独立 job（B1, B2, B3），每个运行约 30 秒
  3. 几乎同时触发 workflow A 和 workflow B
  4. 通过 API 持续记录每个 job 的 queued→running 时间戳
  5. 计算两个 workflow 的调度延迟分布

预期结果:
  - workflow A 和 workflow B 的 jobs 不应出现一方全部完成后另一方才开始的情况
  - 在资源有限时，两个 workflow 的 jobs 应交错获得 runner
  - 任一 workflow 的最后一个 job 开始时间不应显著晚于另一个 workflow 的最后一个 job（容差 < 60 秒）

验证点:
  - [正向] 两个 workflow 的 jobs 有交错 running 的时间段
  - [正向] 两个 workflow 的首个 job 开始时间差 < 30 秒
  - [非功能] 最后一个 job 开始时间差 < 60 秒

清理:      重置 fixture 仓库
