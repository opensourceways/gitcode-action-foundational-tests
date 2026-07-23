用例 ID:   SEC-INJECT-02-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-012
标题:      提交信息中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - fork 侧提交含 shell 元字符的 commit message
  - workflow 将 `${{ atomgit.event.head_commit.message }}` 直接插入 run:

操作步骤:
  1. fork 侧 commit message 含反引号命令替换或分号+命令
  2. push 触发 workflow
  3. 检查日志

预期结果:
  - commit message 中的附加命令不产生执行副作用

验证点:
  - [负向] 日志中不出现注入命令执行痕迹
  - [负向] 反引号命令替换不被执行

清理:      fixture
