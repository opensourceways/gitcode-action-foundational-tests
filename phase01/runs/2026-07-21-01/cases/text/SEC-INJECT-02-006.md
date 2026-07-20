用例 ID:   SEC-INJECT-02-006
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-013
标题:      通过环境变量安全引用不可信输入应不触发脚本注入

前置条件:
  - workflow 使用 env 中间变量安全引用 PR 标题

操作步骤:
  1. `env: { PR_TITLE: ${{ atomgit.event.pull_request.title }} }`
  2. `run: echo "$PR_TITLE"`（通过 $PR_TITLE，非 ${{ }} 直接插入）
  3. PR 标题含 `"; ls /"` 等元字符

预期结果:
  - shell 元字符被当作字面字符串，不被解释执行
  - workflow 正常完成

验证点:
  - [正向] env 中间变量方式引用，ls 不被执行
  - [正向] workflow 正常完成
  - [正向] 变量值保留原始字符

清理:      fixture
