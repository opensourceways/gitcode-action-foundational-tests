用例 ID:   REL-PUSH-DEDUP-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-030
母意图:    —
标题:      同一 push 连推的触发去重/幂等与并发触发排队公平性

前置条件:
  - 仓库已启用 push 触发
  - 支持快速连续推送

操作步骤:
  1. 在 10 秒内对同一分支连续推送 3 次 commit
  2. 观察 workflow 触发次数与 run 状态

预期结果:
  - 同一 push 事件不应触发多个重复 run
  - 若去重失败，则多余 run 应被排队而非丢弃

验证点:
  - [正向] 3 次连推产生的 run 数 <= 3（期望去重为 1 或 3 个有序 run）
  - [负向] 无 run 被静默丢弃
  - [nonfunctional] run 排队公平

清理:      重置 fixture 仓库
