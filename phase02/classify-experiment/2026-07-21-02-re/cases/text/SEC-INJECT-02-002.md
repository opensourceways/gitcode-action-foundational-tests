用例 ID:   SEC-INJECT-02-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-010
标题:      PR 正文中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - fork PR 正文包含多行 shell 注入 payload
  - workflow 将 `${{ atomgit.event.pull_request.body }}` 直接插入 run:

操作步骤:
  1. fork PR 正文含 $() 命令替换、反引号命令替换
  2. 检查 job 日志

预期结果:
  - PR 正文中的 shell 元字符不被解释执行

验证点:
  - [负向] 日志中不出现注入命令输出
  - [负向] $(cmd) 命令替换不被执行
  - [负向] 反引号命令替换不被执行

清理:      fixture
