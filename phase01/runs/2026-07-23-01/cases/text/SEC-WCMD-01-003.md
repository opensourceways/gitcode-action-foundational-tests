用例 ID:   SEC-WCMD-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-030
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      ATOMGIT_ENV 不被不可信输入污染提权

前置条件:
  - 仓库支持 workflow 环境变量注入

操作步骤:
  1. 提交一个 workflow，将含换行/协议控制字符的不可信值写入 ATOMGIT_ENV
  2. 触发 workflow 并检查后续 step 的环境变量

预期结果:
  - 不可信值写入 ATOMGIT_ENV 时不应注入额外环境变量
  - 多行/换行注入被安全处理

验证点:
  - [负向] 含换行/协议控制字符的不可信值写入 ATOMGIT_ENV 时，不应注入计划外的环境变量
  - [非功能] 多行值应经随机 delimiter 等机制安全写入

清理:      重置 fixture 仓库
