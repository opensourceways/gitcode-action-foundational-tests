用例 ID:   REL-CANCEL-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-019
标题:      手动取消 sleep step，step 收到终止信号且清理步骤仍执行

前置条件:
  - step sleep 600，手动取消运行

操作步骤:
  1. 取消后 step 进程收到 SIGTERM
  2. 10s 内未退出则 SIGKILL
  3. if: always() 清理步骤正常执行
  4. job status = cancelled

预期结果:
  - 被取消 step 在 10s 内终止
  - 清理步骤正常执行

验证点:
  - [正向] step 10s 内终止
  - [正向] 清理步骤执行
  - [负向] 不 stuck > 120s

清理:      fixture
