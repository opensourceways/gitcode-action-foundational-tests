用例 ID:   COMPAT-CONCUR-01-003
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-005
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      concurrency preemption enable 行为差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，配置 `concurrency.preemption.enable: true`
  2. 触发该 workflow 的多个并发运行
  3. 观察超上限时的抢占行为

预期结果:
  - GitHub 行为：cancel-in-progress 为 true 时，新运行取消旧运行
  - GitCode 行为：preemption 配置可能不被识别或行为不同
  - 应明确记录差异

验证点:
  - [正向] 系统接受或拒绝 preemption 配置时应给出明确提示
  - [负向] 不通过 preemption 配置被静默忽略

清理:      无
