用例 ID:   REL-RUNNER-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-012
标题:      step 尝试分配超过 runner 可用内存时被 OOM kill 且 job 标记失败

前置条件:
  - small runner (2C/8G)
  - step 逐步分配内存超过 8GB

操作步骤:
  1. node -e 循环分配内存至超过 8GB
  2. 验证进程被 OOM killer 终止
  3. 验证 job status = failure

预期结果:
  - OOM kill → exit code 137
  - job status = failure
  - runner 继续存活

验证点:
  - [正向] OOM step 非零退出
  - [正向] job status = failure
  - [负向] reset runner 不崩溃

清理:      fixture
