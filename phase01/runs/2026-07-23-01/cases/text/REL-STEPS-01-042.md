用例 ID:   REL-STEPS-01-042
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-042
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      超多 step——单 job 内 50 个 step 应全部串行执行无丢失

前置条件:
  - 仓库具备 workflow 创建权限

操作步骤:
  1. 创建含单 job 50 个 step 的 workflow 并保存/触发

预期结果:
  - 若平台限制≤16，则应明确拒绝或自动拆分
  - 50 个 step 按顺序执行无丢失

验证点:
  - [正向] 50 个 step 全部出现在运行详情页
  - [正向] 每个 step 日志包含唯一标识
  - [负向] 不应出现 step 丢失或顺序错乱

清理:      无需特殊清理
