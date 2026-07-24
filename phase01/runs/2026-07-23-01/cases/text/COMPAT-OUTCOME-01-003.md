# 用例归档

用例 ID:   COMPAT-OUTCOME-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-035
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      outcome 与 conclusion 在 job 条件判断中不应互换语义

前置条件:
  - 仓库已启用 workflow

操作步骤:
  1. 创建一个 workflow_dispatch 触发的 workflow
  2. 配置 job A 包含一个 `continue-on-error: true` 且会失败的 step
  3. 配置 job B 依赖 job A，在 needs 中使用不同的条件上下文判断 job A 的状态
  4. 分别测试使用 outcome 语义和 conclusion 语义的场景
  5. 手动触发该 workflow

预期结果:
  - outcome 反映 step 的真实执行结果（failure）
  - conclusion 反映 step 的最终判定（success，因 continue-on-error）
  - job 级别的状态应基于 conclusion（即 success），使 needs 条件判断可继续
  - 系统不应将 outcome 与 conclusion 混用，导致条件判断行为与 GitHub 不一致

验证点:
  - [正向] job A 的 outcome 保持为 failure
  - [正向] job A 的 conclusion 为 success
  - [正向] job B 的 needs 条件基于 conclusion 判断时认为 job A 成功
  - [负向] 不应出现 outcome 与 conclusion 被互换使用导致的误判

清理:      重置 fixture 仓库
