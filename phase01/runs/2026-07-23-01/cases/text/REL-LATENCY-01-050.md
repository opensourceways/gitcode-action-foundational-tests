用例 ID:   REL-LATENCY-01-050
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-050
母意图:    —
标题:      调度延迟基准——queued→running P50/P95 等待时间

前置条件:
  - 仓库具备 workflow 运行权限
  - runner 池存在空闲 runner

操作步骤:
  1. 在空闲 runner 条件下连续触发 30 次单 job workflow，记录 queued→running 延迟

预期结果:
  - P95 延迟有界
  - 形成可复现的基准数据集

验证点:
  - [正向] P95≤60s
  - [负向] 不应出现 runner 空闲但 job 死等>10min

清理:      无需特殊清理
