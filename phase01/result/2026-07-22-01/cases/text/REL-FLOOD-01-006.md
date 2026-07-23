用例 ID:   REL-FLOOD-01-006
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-036
母意图:    —
标题:      并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失

前置条件:
  - 仓库已启用 Actions
  - 具备同时发起 10 个 push 的自动化能力
  - runner 资源总量足以支撑 10 个并发 job

操作步骤:
  1. 准备 10 个不同的 commit，每个修改不同文件以避免冲突
  2. 在极短时间窗口内（< 1 秒）将这 10 个 commit 同时 push 到同一分支
  3. 通过 API 查询该仓库的 workflow runs 列表
  4. 等待所有运行进入终态（COMPLETED / FAILED / CANCELED）

预期结果:
  - 10 个 push 各触发 1 个 workflow run，总计 10 个 run 全部被创建且无静默丢失
  - 每个 run 均可通过 API 查询到状态与日志
  - 无重复运行或合并运行（除非平台设计如此）

验证点:
  - [正向] runs 总数等于 10
  - [正向] 每个 run 的触发事件均为 Push
  - [负向] 无 run 状态为 UNKNOWN 或无法查询

清理:      重置 fixture 仓库
