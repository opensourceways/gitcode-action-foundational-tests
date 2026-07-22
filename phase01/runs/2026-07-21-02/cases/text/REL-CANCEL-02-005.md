用例 ID:   REL-CANCEL-02-005
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-038
标题:      取消后运行终态收敛与 runner 资源释放时限

前置条件:
  - 仓库配置了支持长时间运行的 fixture
  - workflow 含一个持续运行 step（如 sleep 180s）与 post 清理步骤

操作步骤:
  1. 触发该 workflow 运行
  2. 在 step 进入 running 状态约 30s 后，手动执行 Cancel 操作
  3. 连续轮询运行状态（每 5s，共 24 次，覆盖 120s 窗口）
  4. 记录状态变化时序与终态值
  5. 取消后每 10s 触发一次探针 job，记录 runner 首次成功调度时刻

预期结果:
  - 手动 Cancel 后，运行状态在有限时间内稳定收敛到 cancelled 终态
  - 终态不反复、不错标为 success 或 failure
  - runner 资源在状态收敛后合理时限内释放，可接受新 job 调度

验证点:
  - [正向] 取消后运行终态 = cancelled，且连续 5 次轮询状态一致（稳定不跳变）
  - [负向] 不应出现「取消成功但状态仍是 running/queued」的情况
  - [负向] 不应错标为 success/failure，不应无限占用 runner 导致新 job 无法调度
  - [非功能] 从点击 Cancel 到终态 cancelled 的时延 ≤60s；runner 释放后能在 60s 内成功调度新探针 job

清理:      fixture
