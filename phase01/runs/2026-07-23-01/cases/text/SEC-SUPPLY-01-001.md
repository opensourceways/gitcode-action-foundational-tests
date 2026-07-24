用例 ID:   SEC-SUPPLY-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
参照来源:  inputs/gitcode-spec/
母意图:    —
标题:      第三方 Action 引用应支持完整 commit hash 固定

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，使用完整 commit SHA 引用第三方 Action
  2. 触发 workflow

预期结果:
  - 完整 commit SHA 引用可成功执行 action
  - commit SHA 不匹配时 job 应失败或拒绝执行

验证点:
  - [正向] 完整 commit SHA 引用可成功执行 action
  - [负向] commit SHA 不匹配或分支被重写时，job 应失败或拒绝执行

清理:      重置 fixture 仓库
