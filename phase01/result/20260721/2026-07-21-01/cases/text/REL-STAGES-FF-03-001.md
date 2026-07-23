用例 ID:   REL-STAGES-FF-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-053
标题:      stages 中前一个 stage 的 job 失败且 fail_fast=true 时后续 stage 全部跳过

前置条件:
  - 3 个 stages: build → test → deploy
  - build stage fail_fast=true，故意 fail

操作步骤:
  1. 定义 build stage 含一个 exit 1 的 job
  2. 定义 test 和 deploy stage 各含正常 job
  3. 触发 workflow，观察 stage 间行为

预期结果:
  - build job = failure
  - test 和 deploy 的 job 状态 = skipped
  - 不应进入 queued 状态

验证点:
  - [正向] build=failure, test=skipped, deploy=skipped
  - [负向] test/deploy 不进入 queued

清理:      none
