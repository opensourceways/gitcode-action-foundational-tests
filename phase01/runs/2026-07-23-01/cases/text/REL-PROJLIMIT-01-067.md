用例 ID:   REL-PROJLIMIT-01-067
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-067
母意图:    —
标题:      项目级 workflow 并发上限——200 条同时触发时全部完成无丢失

前置条件:
  - 仓库具备 workflow 触发权限
  - 目标项目未设置额外的仓库级并发限制（仅依赖平台全局上限）

操作步骤:
  1. 在 60s 内通过 API 并发触发 200 次同一 workflow（workflow_dispatch）
  2. 每次触发携带唯一标识（如递增序号）以便后续对账
  3. 等待全部 200 次触发进入终态（queued → running → completed/failed/cancelled）

预期结果:
  - 200 次触发全部进入终态，无静默丢失
  - 失败数 = 0
  - 排队数 = 0（平台应支持 200 条同时运行，无需排队）
  - 总耗时（从首次触发到最后一次终态）≤ 60 min

验证点:
  - [正向] completed_count = 200
  - [正向] failed_count = 0
  - [正向] queued_count = 0（200 条应全部立即进入 running）
  - [正向] lost_count = 0
  - [负向] 不应出现触发后无对应 run 记录（丢失）
  - [负向] 不应因并发超限而直接返回 429/500 导致触发失败

清理:      无需特殊清理
