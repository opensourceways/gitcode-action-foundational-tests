用例 ID:   REL-FAIR-01-044
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-044
母意图:    —
标题:      并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度

前置条件:
  - 仓库具备同时触发多个 workflow 的权限

操作步骤:
  1. 同时触发 workflow X 和 workflow Y，各含 3 个 jobs，每 job sleep 30 秒

预期结果:
  - 2 个 workflow 的 jobs 启动时间差 ≤60 秒
  - 无单个 workflow 独占所有 Runner

验证点:
  - [正向] 启动时延差≤60 秒
  - [负向] 不应出现 workflow X 全部完成后 workflow Y 才开始

清理:      无需特殊清理
