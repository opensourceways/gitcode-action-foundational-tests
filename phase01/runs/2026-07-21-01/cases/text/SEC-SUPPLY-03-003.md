用例 ID:   SEC-SUPPLY-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-031
母意图:    —
标题:      composite action 内部的 run 步骤中引用不可信 inputs 不应导致注入

前置条件:
  - 存在可调用 composite action 的 workflow
  - composite action 内部有 run 步骤

操作步骤:
  1. 传入含注入字符的 inputs 到 composite action
  2. 观察 action 内部的 run 是否被注入
  3. 对比 env 中间变量模式与直接引用模式的差异

预期结果:
  - 含注入字符的 inputs 在 composite action 内部直接用于 run 时不应执行注入命令
  - 通过 env 中间变量使用的 inputs 应安全

验证点:
  - [负向] 含注入字符的 inputs 传入 composite action 直接用于 run 不应执行注入命令
  - [正向] composite action 内通过 env 中间变量使用的 inputs 应安全

清理:      none
