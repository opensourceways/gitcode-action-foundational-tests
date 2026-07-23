用例 ID:   SEC-TOKEN-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-024
母意图:    —
标题:      ATOMGIT_TOKEN 触发的操作不应产生递归 workflow 运行

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 中使用 ATOMGIT_TOKEN 推送代码
  2. 观察是否触发新的 workflow 运行
  3. 验证是否仅产生 1 个 run

预期结果:
  - 使用 ATOMGIT_TOKEN 执行的 git push 不应递归触发新 workflow run
  - 使用 ATOMGIT_TOKEN 创建的 PR 不应自动触发该 PR 的 workflow

验证点:
  - [负向] git push 后不应产生新的 workflow run
  - [负向] PR 创建后不应自动触发该 PR 的 workflow

清理:      none
