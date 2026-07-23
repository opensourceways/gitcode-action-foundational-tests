用例 ID:   REL-RACE-01-048
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-048
母意图:    —
标题:      取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定

前置条件:
  - 仓库存在正在运行的 workflow

操作步骤:
  1. job A 运行中被手动取消，job B needs A 且 if: failure()

预期结果:
  - job A 状态=cancelled
  - job B 状态=skipped
  - job B 不应执行

验证点:
  - [正向] job A 状态=cancelled
  - [正向] job B 状态=skipped
  - [负向] job B 不应执行

清理:      无需特殊清理
