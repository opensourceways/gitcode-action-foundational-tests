用例 ID:   SEC-INJ-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-010
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      不可信分支名不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一个分支名含 shell 元字符的 PR

操作步骤:
  1. 提交一个 workflow，在 run 脚本中直接内联引用分支名
  2. 触发该 workflow

预期结果:
  - 分支名中的特殊字符不应被解释为 shell 元字符
  - 表达式值应被安全求值

验证点:
  - [负向] 含特殊字符的分支名绝不应被解释为 shell 命令
  - [非功能] 安全写法（中间环境变量）应正常生效

清理:      重置 fixture 仓库
