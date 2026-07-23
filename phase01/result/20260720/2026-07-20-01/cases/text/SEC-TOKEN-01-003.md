用例 ID:   SEC-TOKEN-01-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-024
标题:      ATOMGIT_TOKEN 触发的操作不应产生递归 workflow 运行
前置条件:  仓库 workflow 同时监听 push 事件
操作步骤:
  1. workflow 中使用 ATOMGIT_TOKEN 推送新 commit
  2. 观察是否触发新的 workflow 运行
  3. 使用 token 创建 PR 或 Issue 评论
预期结果: token 触发的操作不产生递归 workflow
验证点:
  - [负向] token 推送后不触发新的 workflow run
  - [负向] token 创建 PR 后不触发该 PR 的 workflow
  - [正向] 仅产生 1 个 workflow run（非链式触发）
清理:      fixture
