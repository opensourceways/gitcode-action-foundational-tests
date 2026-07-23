用例 ID:   REL-SCHED-01-057
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-057
母意图:    —
标题:      资源调度状态一致性——空闲 runner 存在时 job 不应死等

前置条件:
  - runner 池存在空闲 runner

操作步骤:
  1. 连续触发 10 次单 job workflow，每次完成后等待 runner 空闲再触发下一次

预期结果:
  - 10 次全部 queued→running ≤60s
  - 平均≤30s

验证点:
  - [正向] 10 次全部≤60s
  - [非功能] 平均≤30s
  - [负向] 不应出现 runner 空闲但 job 死等>5min

清理:      无需特殊清理
