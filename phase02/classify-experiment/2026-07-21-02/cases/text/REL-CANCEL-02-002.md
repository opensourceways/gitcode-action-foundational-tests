用例 ID:   REL-CANCEL-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-020
标题:      stages.fail_fast=true 时，stage 内第一个 job 失败后同一 stage 内其他仍在运行的 job 被取消

前置条件:
  - 2-stage workflow
  - stage1 含 job A（快失败 exit 1）和 job B（sleep 120）
  - stage2 含 job C
  - stage1.fail_fast=true

操作步骤:
  1. 触发 workflow，job A 立即失败
  2. 验证 job B 被取消（收到取消信号）
  3. 验证后续 stage 全部跳过
  4. workflow 终态为 failure

预期结果:
  - job B 状态变更为 cancelled
  - 后续 stage 所有 job 为 skipped
  - workflow 终态为 failure

验证点:
  - [正向] job B 状态变更为 cancelled
  - [正向] 后续 stage job 全部 skipped
  - [负向] job B 不跑到 completed(success)

清理:      fixture
