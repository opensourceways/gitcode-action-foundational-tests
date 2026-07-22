用例 ID:   SEC-ENV-POLLUTE-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-024
母意图:    —
标题:      工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权

前置条件:
  - workflow 接收来自 PR 标题/评论等不可信输入
  - 存在后续高权限 step

操作步骤:
  1. 在 PR 标题中注入恶意字符串（如包含换行符的伪造 workflow 命令）
  2. 在 workflow 中将 PR 标题写入 $ATOMGIT_ENV
  3. 观察后续 step 的环境变量与行为

预期结果:
  - 不可信输入写入 ATOMGIT_ENV 时不应解析执行注入命令
  - 后续 step 不应因写协议污染而获得提权

验证点:
  - [负向] 无注入命令被执行
  - [负向] 环境变量不含恶意换行注入内容

清理:      重置 fixture 仓库
