用例 ID:   SEC-TOCTOU-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-031
母意图:    SEC-TOCTOU-01-001
标题:      评论触发不应绕过代码固定与 PR 审批

前置条件:
  - 仓库配置了 issue_comment 触发 workflow

操作步骤:
  1. 提交一个由 issue_comment 触发的高权限 workflow
  2. 在评论触发后、执行前推送新 commit
  3. 观察运行是否执行了最新 commit 而非触发时的 commit

预期结果:
  - 评论触发不应绕过代码固定
  - 运行应执行评论触发时刻锁定的 commit SHA

验证点:
  - [负向] 评论触发后推送的新 commit 绝不应被该次特权运行自动执行
  - [正向] 运行日志中的 commit SHA 与触发时刻一致

清理:      重置 fixture 仓库
