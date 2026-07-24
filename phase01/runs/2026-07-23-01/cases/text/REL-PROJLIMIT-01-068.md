用例 ID:   REL-PROJLIMIT-01-068
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-068
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      项目级 workflow 并发上限越界——201 条同时触发时至少一条进入排队

前置条件:
  - 仓库具备 workflow 触发权限
  - 目标项目未设置额外的仓库级并发限制（仅依赖平台全局上限 200）

操作步骤:
  1. 在 60s 内通过 API 并发触发 201 次同一 workflow（workflow_dispatch）
  2. 每次触发携带唯一标识（如递增序号）以便后续对账
  3. 等待全部 201 次触发进入终态（queued → running → completed/failed/cancelled）

预期结果:
  - 201 次触发全部进入终态，无静默丢失
  - 失败数 = 0
  - 至少有一条 run 在触发后进入 queued 状态（排队等待），而非立即 running
  - 总耗时（从首次触发到最后一次终态）≤ 60 min

验证点:
  - [正向] completed_count = 201
  - [正向] failed_count = 0
  - [正向] queued_count ≥ 1（超出 200 上限部分应排队）
  - [正向] lost_count = 0
  - [负向] 不应出现触发后无对应 run 记录（丢失）
  - [负向] 不应因并发超限而直接返回 429/500 导致触发失败

清理:      无需特殊清理
