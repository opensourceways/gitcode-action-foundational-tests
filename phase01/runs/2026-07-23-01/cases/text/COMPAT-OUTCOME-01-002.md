# 用例归档

用例 ID:   COMPAT-OUTCOME-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-035
母意图:    —
标题:      continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success

前置条件:
  - 仓库已启用 workflow

操作步骤:
  1. 创建一个 workflow_dispatch 触发的 workflow
  2. 配置一个 step，显式设置 `continue-on-error: true`
  3. 该 step 的 run 脚本以非零退出码结束（如 `exit 1`）
  4. 在后续 step 中读取该 step 的 outcome 和 conclusion
  5. 手动触发该 workflow

预期结果:
  - 该 step 的 outcome 为 failure（实际执行失败）
  - 该 step 的 conclusion 为 success（因 continue-on-error 被覆盖为成功）
  - job 整体继续执行后续 step，不应被中断
  - 语义与 GitHub Actions 一致

验证点:
  - [正向] 失败 step 的 outcome 为 failure
  - [正向] 失败 step 的 conclusion 为 success
  - [正向] 后续 step 正常执行
  - [正向] job 最终状态为 success（若无其他失败）

清理:      重置 fixture 仓库
