用例 ID:   COMPAT-CONCUR-01-004
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-005
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      concurrency preemption events 越界时行为差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，配置 `concurrency.preemption.events` 为 11 个（越界值）
  2. 提交该 workflow
  3. 观察系统校验行为

预期结果:
  - GitHub 行为：events 越界时应被拒绝并给出有效范围提示
  - GitCode 行为：可能不支持 preemption events 配置
  - 应明确记录差异

验证点:
  - [正向] 系统对越界值给出明确报错
  - [正向] 报错包含有效范围提示

清理:      无
