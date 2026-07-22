用例 ID:   REL-RERUN-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-027
标题:      Re-run all jobs 后，ATOMGIT_RUN_ID 和 ATOMGIT_RUN_NUMBER 更新为新值，atomgit.sha 保持原值

前置条件:
  - 先触发一次 Run
  - 然后 Re-run all jobs

操作步骤:
  1. 触发 Run #1，记录 run_id、run_number、commit_sha
  2. Re-run all jobs 触发 Run #2
  3. 比对两次 Run 的上下文变量

预期结果:
  - 新 run_id != 旧 run_id
  - 新 run_number > 旧 run_number
  - 新旧 atomgit.sha 相同

验证点:
  - [正向] run_id 不同
  - [正向] run_number 递增
  - [正向] sha 保持一致

清理:      fixture
