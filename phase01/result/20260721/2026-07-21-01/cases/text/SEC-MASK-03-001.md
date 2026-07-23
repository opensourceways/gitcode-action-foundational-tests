用例 ID:   SEC-MASK-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
母意图:    —
标题:      Secret 值直接 echo 到日志时应被脱敏为 ***

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 push 触发的基础 workflow

操作步骤:
  1. 在 workflow step 中通过 ${{ secrets.TEST_SECRET }} 引用 secret 并 echo 到日志
  2. 将 secret 值赋给 env 中间变量后 echo 该变量
  3. 在同一 job 内多次引用同一 secret
  4. 通过 API 拉取 job 日志全文搜索已知 secret 明文

预期结果:
  - 日志中所有出现 secret 值的位置均应被替换为 ***
  - 搜索已知 secret 明文值在日志全文中的命中数 = 0

验证点:
  - [负向] job 日志全文搜索 TEST_SECRET 已知明文值，命中数 = 0
  - [负向] 同一 job 内多次引用同一 secret，每次出现均应被遮蔽
  - [正向] echo 非 secret 文本时日志正常显示

清理:      none
