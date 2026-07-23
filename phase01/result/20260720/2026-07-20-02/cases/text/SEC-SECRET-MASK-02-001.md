用例 ID:   SEC-SECRET-MASK-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
标题:      Secret 值直接 echo 到日志时应被脱敏为 ***

前置条件:
  - 仓库配置了 Secret（TEST_SECRET，值已知）
  - workflow 中将 Secret 值 echo 到日志

操作步骤:
  1. 在 workflow 中 `run: echo "${{ secrets.TEST_SECRET }}"`
  2. API 拉取 job 日志全文搜索 Secret 原始值

预期结果:
  - 日志中所有出现 Secret 的位置显示 *** 或等效遮蔽
  - 全文搜索 Secret 原始值命中数为 0

验证点:
  - [负向] 日志中不出现 Secret 明文
  - [正向] 非 Secret 文本正常显示
  - [负向] 多次引用同一 Secret 均被遮蔽

清理:      fixture
