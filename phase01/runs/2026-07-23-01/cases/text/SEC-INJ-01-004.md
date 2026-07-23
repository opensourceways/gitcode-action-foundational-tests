用例 ID:   SEC-INJ-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-012
母意图:    —
标题:      不可信 commit message 不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一条 commit message 含反引号或分号的 push

操作步骤:
  1. 提交一个由 push 触发的 workflow，在 run 中引用 commit message
  2. 推送一条含 shell 元字符的 commit

预期结果:
  - commit message 中的 shell 元字符不应被解释为命令执行
  - 安全写法（中间环境变量）应正常生效

验证点:
  - [负向] 含反引号或分号的 commit message 绝不应被解释为命令执行
  - [非功能] 安全写法（中间环境变量）应正常生效

清理:      重置 fixture 仓库
