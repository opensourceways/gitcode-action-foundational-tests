用例 ID:   REL-CONC-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-001
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      concurrency.max=5 时同时触发 5 个运行应全部进入执行态

前置条件:
  - 仓库已配置 concurrency.max=5 的 workflow

操作步骤:
  1. 同时通过 API 触发 5 次该 workflow

预期结果:
  - 5 个运行均进入 in_progress 状态
  - 全部在合理时间内完成

验证点:
  - [正向] 5 个运行状态均为 completed(success)
  - [非功能] queued→in_progress 调度时延 ≤60 秒

清理:      无需特殊清理
