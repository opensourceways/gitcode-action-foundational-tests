用例 ID:   SEC-INJECT-01-006
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-030
母意图:    —
标题:      第三方 action 的输入参数中的不可信值不应导致 action 内部代码注入

前置条件:
  - 仓库中存在使用第三方 action 的 workflow
  - action 接收 `with:` 参数
  - 外部 fork PR 的标题包含 shell 特殊字符

操作步骤:
  1. 创建 fork PR，标题包含 shell 注入字符：`fix"; echo ACTION_INJECTED; #`
  2. workflow 使用某个 action，将其 `with:` 参数绑定到 `${{ atomgit.event.pull_request.title }}`
  3. 触发 pull_request 事件
  4. 观察 action 日志中是否出现 `ACTION_INJECTED` 输出
  5. 对比：直接使用内联 `run:` 脚本的注入行为和通过 action `with:` 参数传递的行为

预期结果:
  - action 的 `with:` 参数中的不可信输入应被当作纯数据处理，不应被 action 内部二次解释为代码
  - 若 action 的 JavaScript runner 环境天然免疫 shell 注入（不经过 shell），注入不应成功
  - 若 action 自身 `exec()` 了传入参数，注入行为与内联脚本一致
  - action 应正常完成（或将注入字符作为合法字符串处理）

验证点:
  - [负向] action 日志中不应出现 `ACTION_INJECTED`（注入命令不应在 action 内执行）
  - [负向] with 参数中的不可信输入不应被 action 执行引擎解释为代码
  - [正向] action 应正常完成或将注入字符作为合法字符串处理
  - [负向] 不应出现因 action 内部注入导致的额外副作用

清理:      fixture
