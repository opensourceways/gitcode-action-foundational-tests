用例 ID:   SEC-INJECT-03-008
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-041
母意图:    —
标题:      提交者 email 地址作为不可信输入不应导致 shell 注入

前置条件:
  - 存在 push 触发的 workflow
  - 攻击者可设置任意 git user.email

操作步骤:
  1. 攻击者设置 git user.email 为含 shell 元字符的地址
  2. workflow 中直接引用 ${{ atomgit.event.head_commit.author.email }} 到 run 中
  3. 观察是否触发命令执行

预期结果:
  - email 地址中的 shell 元字符不应被解释执行
  - 若直接引用不安全，env 中间变量模式应有效

验证点:
  - [负向] email 中反引号命令替换不应被解释执行
  - [负向] 日志中不出现因 email 注入导致的额外命令输出
  - [正向] 通过 env 中间变量引用 email 应安全

清理:      none
