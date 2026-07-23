用例 ID:   SEC-CMDINJ-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
母意图:    —
标题:      issue/PR 评论内容不可直接插进 run 脚本导致命令注入

前置条件:
  - 仓库存在 workflow 监听 pull_request_comment 事件
  - 存在一个外部 fork 的 PR

操作步骤:
  1. 在该 PR 下发表评论，内容包含 shell 元字符（如反引号、分号、管道符）
  2. 触发 pull_request_comment workflow，该 workflow 将评论内容通过表达式插入 run 脚本
  3. 观察 workflow 执行结果与日志

预期结果:
  - 评论内容中的特殊字符被转义或表达式求值结果以字符串字面量形式传入
  - 系统不应执行评论中嵌入的命令
  - 运行日志不暴露内部环境信息

验证点:
  - [负向] 未因评论内容执行非预期命令
  - [负向] 日志中不出现因命令注入导致的异常系统输出
  - [正向] workflow 正常完成或按预期失败（非注入导致的任意执行）

清理:      重置 fixture 仓库
