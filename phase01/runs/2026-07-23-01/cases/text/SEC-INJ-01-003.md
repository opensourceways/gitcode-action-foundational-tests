用例 ID:   SEC-INJ-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一条包含 shell 元字符的评论

操作步骤:
  1. 提交一个由 issue_comment 触发的 workflow，在 run 中引用评论 body
  2. 提交一条含 shell 元字符的评论触发 workflow

预期结果:
  - 评论 body 中的 shell 元字符不应被解释为命令执行
  - 即使评论被编辑，重新触发时仍应维持安全过滤

验证点:
  - [负向] 含 shell 元字符的评论内容绝不应被解释为命令执行
  - [非功能] 即使评论被编辑，重新触发时仍应维持安全过滤

清理:      重置 fixture 仓库
