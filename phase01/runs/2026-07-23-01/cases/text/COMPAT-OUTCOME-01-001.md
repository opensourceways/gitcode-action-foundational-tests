# 用例归档

用例 ID:   COMPAT-OUTCOME-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-035
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      continue-on-error false 时 outcome 与 conclusion 应均为 failure

前置条件:
  - 仓库已启用 workflow

操作步骤:
  1. 创建一个 workflow_dispatch 触发的 workflow
  2. 配置一个 step，显式设置 `continue-on-error: false`（或默认不写）
  3. 该 step 的 run 脚本以非零退出码结束（如 `exit 1`）
  4. 在后续 step 中通过 `${{ atomgit.step.status }}` 或上下文读取该 step 的状态
  5. 手动触发该 workflow

预期结果:
  - 该 step 失败后，job 整体标记为失败
  - outcome（执行结果）与 conclusion（最终判定）均为 failure
  - 由于 continue-on-error 为 false，两者不应出现差异

验证点:
  - [正向] 失败 step 的 outcome 为 failure
  - [正向] 失败 step 的 conclusion 为 failure
  - [正向] job 整体状态为 failure

清理:      重置 fixture 仓库
