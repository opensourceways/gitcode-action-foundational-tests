用例 ID:   SEC-CMDINJ-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-009
母意图:    —
标题:      PR 正文不可直接插进 run 脚本导致命令注入

前置条件:
  - 仓库存在 workflow 监听 pull_request_target 事件
  - 存在一个外部 fork 的 PR

操作步骤:
  1. 创建或更新一个 PR，其正文包含 shell 元字符（如反引号、分号、美元符号）
  2. 触发 pull_request_target workflow，该 workflow 将 PR 正文通过表达式插入 run 脚本
  3. 观察 workflow 执行结果与日志

预期结果:
  - PR 正文中的特殊字符被转义或表达式求值结果以字符串字面量形式传入
  - 系统不应执行正文中嵌入的命令
  - 运行日志不暴露内部环境信息

验证点:
  - [负向] 未因 PR 正文内容执行非预期命令
  - [负向] 日志中不出现因命令注入导致的异常系统输出
  - [正向] workflow 正常完成或按预期失败（非注入导致的任意执行）

清理:      重置 fixture 仓库
