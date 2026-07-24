用例 ID:   SEC-SUPPLY-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
参照来源:  inputs/gitcode-spec/syntax-reference/runner-images-tools.md; inputs/gitcode-spec/writing-pipelines/using-script-commands.md
母意图:    SEC-SUPPLY-01-001
标题:      commit hash 不匹配时第三方 Action 应被拒绝执行

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，使用一个不存在的 commit SHA 引用 Action
  2. 触发 workflow

预期结果:
  - job 进入失败状态或明确拒绝执行
  - 系统不应静默回退到分支 HEAD

验证点:
  - [负向] 错误 commit SHA 绝不应执行 Action
  - [正向] 返回明确的 Action 未找到或 SHA 不匹配错误

清理:      重置 fixture 仓库
