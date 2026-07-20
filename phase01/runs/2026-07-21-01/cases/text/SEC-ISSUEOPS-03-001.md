用例 ID:   SEC-ISSUEOPS-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-039
母意图:    —
标题:      issue_comment 触发器不应绕过 PR 审批机制——IssueOps TOCTOU

前置条件:
  - 仓库有 issue_comment 触发 workflow
  - 管理员在 PR 评论中触发 `/deploy` 命令
  - 攻击者在 workflow 执行前推送恶意代码

操作步骤:
  1. 提交无害 PR
  2. 管理员评论 `/deploy` 触发 issue_comment workflow
  3. 在 workflow 执行前推送恶意 commit
  4. 验证 workflow 执行的代码版本

预期结果:
  - issue_comment 触发不应被用于执行 PR 代码（除非使用 commit SHA 锁定 + label gate）
  - 文档应说明 issue_comment 触发器的安全风险

验证点:
  - [负向] issue_comment 触发后执行的代码应与管理员评论时的 commit 一致
  - [正向] platform 文档是否提及 issue_comment 安全注意事项
  - [正向] labeled activity type 触发 workflow 时应使用审批时的 commit SHA

清理: fixture
