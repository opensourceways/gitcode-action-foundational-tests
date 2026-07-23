用例 ID:   REL-LATENCY-01-050-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-050
母意图:    —
标题:      调度延迟压力——并发 20 个 job 的排队延迟与完成率

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 并发触发 20 个单 job workflow，各 sleep 60s

预期结果:
  - 所有 job 最终完成
  - 无饿死
  - 排队延迟可观测

验证点:
  - [正向] 20 个 job 全部完成
  - [负向] 无 job 被无限饿死

清理:      无需特殊清理
