用例 ID:   SEC-INJECT-03-006
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-013
母意图:    —
标题:      通过环境变量安全引用不可信输入应不触发脚本注入

前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题

操作步骤:
  1. fork 侧创建含 shell 元字符的 PR 标题
  2. workflow 通过 env 中间变量引用 PR 标题后 echo
  3. 观察是否触发命令执行

预期结果:
  - env 中间变量方式引用的含元字符的 PR 标题不触发命令执行
  - shell 元字符被当作字面字符串处理
  - workflow 应正常完成

验证点:
  - [正向] env 中间变量方式引用的含元字符的 PR 标题不触发命令执行
  - [正向] env 中间变量方式的 workflow 正常完成
  - [负向] 日志中不出现注入命令的执行痕迹

清理:      fixture
