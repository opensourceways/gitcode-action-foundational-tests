用例 ID:   SEC-SECRET-MASK-02-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-008
标题:      Secret 包含多行文本时应整体被脱敏

前置条件:
  - 仓库配置了多行 Secret（如 SSH 私钥格式的内容）

操作步骤:
  1. 设置含换行的 Secret（PEM 证书格式）
  2. workflow 中 echo 该 Secret
  3. 逐行搜索 Secret 各行内容

预期结果:
  - 多行 Secret 每一行在日志中均被遮蔽
  - 无一行明文出现在日志中

验证点:
  - [负向] 日志搜索 Secret 各行内容命中数 = 0
  - [负向] 换行转义符不导致还原为实际换行后明文

清理:      fixture
