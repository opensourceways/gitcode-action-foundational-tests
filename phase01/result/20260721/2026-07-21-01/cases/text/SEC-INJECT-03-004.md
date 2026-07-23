用例 ID:   SEC-INJECT-03-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-012
母意图:    —
标题:      提交信息中的不可信输入不应通过 ${{ }} 直接插入 run 导致命令注入

前置条件: 主仓库有 push 触发 workflow，run 中引用 `${{ atomgit.event.commits[0].message }}`

操作步骤:
  1. fork 侧提交代码，commit message 设为 `` `cat /etc/passwd > /tmp/exfil` ``
  2. 向主仓提 PR 触发 workflow
  3. 观察 /tmp/exfil 是否被创建

预期结果: commit message 中的反引号命令替换不应被执行；/tmp/exfil 不应存在

验证点:
  - [负向] job 日志不出现注入命令执行痕迹
  - [负向] runner 文件系统不出现注入命令的产物
  - [正向] workflow 正常完成

清理: fixture
