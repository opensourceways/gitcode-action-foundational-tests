用例 ID:   REL-TIMEOUT-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-010
标题:      多个 job 设置不同 timeout-minutes（5/360），各自按独立时钟超时

前置条件:
  - job A: timeout-minutes=5，step sleep 600
  - job B: timeout-minutes=360，step echo done
  - 两 job 无 needs 依赖

操作步骤:
  1. 同时启动 job A 和 job B
  2. 验证 job A 在 5min ± 30s 内因超时终止
  3. 验证 job B 正常完成（exec 30s 即结束）
  4. 验证 job A 的超时不触发 job B 的取消

预期结果:
  - job A 在 5min ± 30s 内终止
  - job B 正常 success
  - 两 job 超时时钟独立

验证点:
  - [正向] job A 5min 内超时终止
  - [正向] job B 正常 success
  - [负向] job A 的超时不取消 job B

清理:      fixture
