用例 ID:   SEC-INJECT-03-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-010
母意图:    —
标题:      PR 正文中的不可信输入不应通过 ${{ }} 直接插入 run 导致命令注入

前置条件: 主仓库有 pull_request 触发 workflow，run 中直接引用 `${{ atomgit.event.pull_request.body }}`

操作步骤:
  1. fork 侧创建 PR，正文含多行注入 payload（含 `$(whoami)`、反引号命令替换、分号分隔命令）
  2. 触发 pull_request workflow
  3. 观察是否出现注入命令执行痕迹

预期结果:
  - PR 正文中的 $() 命令替换、反引号命令替换、分号注入均不应被执行
  - job 日志不出现注入命令的输出

验证点:
  - [负向] job 日志不出现 whoami 输出或注入命令的副作用
  - [负向] PR 正文中的 shell 元字符不被解释执行为命令
  - [正向] workflow 正常完成或报明确安全错误

清理: fixture
