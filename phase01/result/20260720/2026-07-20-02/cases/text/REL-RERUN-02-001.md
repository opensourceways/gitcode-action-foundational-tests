用例 ID:   REL-RERUN-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-025
标题:      Re-run failed jobs 仅失败 job 重执行，成功 job 状态保留

前置条件:
  - jobA success, jobB failure（故意 exit 1）

操作步骤:
  1. 首次运行：A success, B failure
  2. Re-run failed jobs → B 重执行，A 保持原结果
  3. 验证使用原始 commit 配置

预期结果:
  - jobA 保持原 success 不被重跑
  - jobB 重新执行
  - 使用原始配置

验证点:
  - [正向] A 保持 success
  - [正向] B 重新执行
  - [正向] 使用原始配置

清理:      fixture
