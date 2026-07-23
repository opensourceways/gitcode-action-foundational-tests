用例 ID:   REL-CONCUR-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-003
标题:      concurrency max=1, exceed-action=CANCEL 时新触发取消旧运行

前置条件:
  - concurrency max=1, exceed-action=CANCEL
  - 旧 run 有 sleep 180 的长步骤

操作步骤:
  1. 触发 Run1（in_progress, sleep 180）
  2. 10s 后触发 Run2
  3. 验证 Run1 被 cancelled, Run2 进入执行

预期结果:
  - 旧 run 被 cancelled
  - 新 run 在旧 run 取消后 60s 内进入执行
  - 新旧不同时 in_progress

验证点:
  - [正向] 旧 run cancelled
  - [正向] 新 run 执行
  - [负向] 新旧不同时 in_progress

清理:      fixture
