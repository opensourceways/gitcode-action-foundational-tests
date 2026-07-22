用例 ID:   REL-PREEMPT-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-040
标题:      preemption 被抢占 job/run 的终态、日志完整性与 runner 释放时效

前置条件:
  - 仓库配置了 concurrency preemption，参数为 enable=true、max=1、events=[mr_id]
  - workflow 含一个连续打印序号的 step（每 1s 打印一行序号+时间戳，共 300s）与 post 清理步骤

操作步骤:
  1. 触发运行 A，使其进入 running 状态
  2. A running 约 30s 后，在同一 workflow、同一 MR ID 上触发运行 B，使 A 被抢占
  3. 观测 A 的终态与状态稳定性（连续轮询 5 次）
  4. 检查 A 的日志行数与内容完整性（应接近 30 行，含被抢占前最后输出）
  5. 检查 A 的日志/UI 是否有 cancelled/preempted 归因标记
  6. 取消后每 10s 触发一次探针 job，记录 runner 首次成功调度时刻

预期结果:
  - 被抢占 job 的终态稳定为 cancelled（或明确标记为 preempted/cancelled）
  - 日志完整保留至被抢占瞬间，不截断、不丢失
  - UI/日志中有明确「被抢占」归因标记
  - runner 在 job 终止后合理时限内释放并可调度新 job

验证点:
  - [正向] 被抢占 job 终态 = cancelled，且连续 5 次轮询状态一致
  - [正向] 日志完整保留，行数 ≥25 行且含被抢占前最后输出
  - [负向] 被抢占 job 不应错标为 success/failure
  - [负向] 不应日志被截断导致被抢占瞬间的输出丢失
  - [负向] 不应无标记导致用户无法区分「代码失败」与「被抢占」
  - [非功能] 从抢占发生到 runner 释放 ≤60s

清理:      fixture
