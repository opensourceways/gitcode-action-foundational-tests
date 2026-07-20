用例 ID:   SEC-MASK-01-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-008
标题:      Secret 包含多行文本时应整体被脱敏

前置条件:
  - 仓库配置一个多行 Secret（如模拟 SSH 私钥格式）
  - Secret 值包含换行符（\n）

操作步骤:
  1. 在 job 中逐行 echo 多行 Secret 的各部分
  2. 将多行 Secret 通过 cat heredoc 方式输出
  3. 将多行 Secret 通过变量间接引用后 echo
  4. 检查日志中是否出现任何一行 Secret 明文

预期结果:
  - 多行 Secret 的每一行在日志中均被遮蔽为 ***
  - Secret 包含换行符时不出现因换行导致的部分泄露
  - 任何形式的输出（逐行、heredoc、变量间接）均被遮蔽

验证点:
  - [负向] 逐行 echo Secret 各部分 → 每行均被遮蔽
  - [负向] heredoc 输出 Secret → 全部遮蔽
  - [负向] 变量间接引用 → 遮蔽
  - [负向] 日志中搜索 Secret 每一行的明文 → 命中数 = 0

清理:      fixture
