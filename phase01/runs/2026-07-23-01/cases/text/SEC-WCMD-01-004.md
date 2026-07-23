用例 ID:   SEC-WCMD-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-030
母意图:    SEC-WCMD-01-003
标题:      ATOMGIT_OUTPUT 不被不可信输入污染提权

前置条件:
  - 仓库支持 workflow output 传递

操作步骤:
  1. 提交一个 workflow，将含换行/协议控制字符的不可信值写入 ATOMGIT_OUTPUT
  2. 触发 workflow 并检查后续 step 的 output

预期结果:
  - 不可信值写入 ATOMGIT_OUTPUT 时不应注入额外 output 条目
  - 后续 step 不应读取到被劫持的 output

验证点:
  - [负向] 含换行/协议控制字符的不可信值写入 ATOMGIT_OUTPUT 时，不应注入计划外的 output 条目
  - [非功能] 多行值应经安全机制写入

清理:      重置 fixture 仓库
