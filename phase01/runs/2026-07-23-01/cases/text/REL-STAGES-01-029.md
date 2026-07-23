用例 ID:   REL-STAGES-01-029
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-029
母意图:    —
标题:      stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs

前置条件:
  - 仓库具备 stages 使用权限

操作步骤:
  1. 触发含 stage 且 3 个 jobs 并行执行的 workflow，1 个 job 故意失败

预期结果:
  - 失败 job 状态=failure
  - 同阶段其余 jobs 状态=cancelled 或 skipped
  - 不应进入下一阶段

验证点:
  - [正向] 失败 job 状态=failure
  - [正向] 同阶段其余 jobs 状态∈{cancelled, skipped}
  - [负向] 不应进入下一阶段

清理:      无需特殊清理
