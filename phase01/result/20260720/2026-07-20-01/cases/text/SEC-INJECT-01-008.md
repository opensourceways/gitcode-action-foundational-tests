用例 ID:   SEC-INJECT-01-008
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-031
标题:      composite action 内部的 run 步骤中引用不可信 inputs 不应导致注入

前置条件:
  - 仓库定义了 composite action
  - composite action 接收外部 inputs 参数
  - inputs 值可能含 shell 注入字符

操作步骤:
  1. 定义 composite action，内部 run 步骤直接使用 ${{ inputs.user_input }}
  2. 调用方 workflow 传入含 shell 注入字符的 inputs（如 "; ls /"）
  3. 触发 workflow，观察 composite action 执行日志
  4. 验证注入命令是否被执行
  5. 对比 env 中间变量方式引用 inputs 的安全性

预期结果:
  - composite action 内的表达式求值在 shell 前完成
  - 注入字符不应导致额外命令执行
  - env 中间变量方式安全引用 inputs
  - 日志中不出现注入命令的副作用

验证点:
  - [负向] 注入 payload 中的命令不应被执行
  - [正向] composite action 正常完成或产生明确错误
  - [正向] env 中间变量方式安全引用 inputs

清理:      fixture
