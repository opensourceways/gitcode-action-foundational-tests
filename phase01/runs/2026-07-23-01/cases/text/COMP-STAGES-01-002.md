用例 ID:   COMP-STAGES-01-002
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-007
母意图:    —
标题:      fail_fast true 时 stage 内任一 job 失败终止同阶段其余 job

前置条件:
  - workflow 定义含 fail_fast: true 的 stage
  - stage 内至少两个 jobs

操作步骤:
  1. 触发 workflow，使 stage 内一个 job 失败
  2. 观察同 stage 其他 job 的行为

预期结果:
  - 失败的 job 导致同 stage 其他 job 被取消或跳过
  - 后续 stages 被跳过

验证点:
  - [正向] 同 stage 其余 job 被终止
  - [负向] 后续 stage 不应执行

清理:      none
