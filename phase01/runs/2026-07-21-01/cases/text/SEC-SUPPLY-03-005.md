用例 ID:   SEC-SUPPLY-03-005
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-055
母意图:    —
标题:      第三方 action 不应通过 input 默认值窃取 ATOMGIT_TOKEN

前置条件:
  - 存在可调用的 action（含 inputs 定义）
  - action 的 inputs.default 设了敏感上下文引用

操作步骤:
  1. 定义 action，其 inputs.default 设为 ${{ secrets.ATOMGIT_TOKEN }}
  2. 调用方不显式传该 input
  3. 观察实际传给 action 的值

预期结果:
  - action 的 inputs.default 中不应允许引用 secrets.* 上下文
  - 默认值应求值为空而非实际 secret 值
  - 平台应在 action inputs 边界隔离敏感上下文

验证点:
  - [负向] action 的 inputs.default 设为 ${{ secrets.ATOMGIT_TOKEN }}，实际传给 action 的值应为空
  - [负向] action 日志中打印的 input 值不应为有效 token

清理:      none
