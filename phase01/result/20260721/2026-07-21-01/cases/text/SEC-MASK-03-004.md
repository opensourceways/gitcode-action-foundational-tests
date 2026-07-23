用例 ID:   SEC-MASK-03-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-008
母意图:    —
标题:      Secret 包含多行文本时应整体被脱敏

前置条件:
  - 仓库配置了多行 secret MULTILINE_SECRET
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow 中逐行 echo 多行 secret 的各行内容
  2. 将多行 secret 整体 echo 到日志
  3. 通过 API 拉取 job 日志，逐行搜索 secret 各行内容

预期结果:
  - 多行 secret 的每一行在日志中出现时均应被遮蔽为 ***

验证点:
  - [负向] 日志全文逐行搜索 MULTILINE_SECRET 各行值，命中数 = 0
  - [负向] 整体 echo 多行 secret 时各行的明文均不出现

清理:      none
