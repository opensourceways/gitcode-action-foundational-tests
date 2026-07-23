用例 ID:   SEC-SECRET-MASK-02-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-007
标题:      Secret 通过子字符串拼接后 echo 应仍被脱敏

前置条件:
  - 仓库配置了 Secret（COMPOUND_SECRET，值如 "abcdefgh"）

操作步骤:
  1. 将 secret 拆为两半：`FIRST=$(echo "${{ secrets.COMPOUND_SECRET }}" | cut -c1-4)`
  2. `SECOND=$(echo "${{ secrets.COMPOUND_SECRET }}" | cut -c5-)`
  3. `echo "${FIRST}${SECOND}"`
  4. 搜索日志中完整 Secret 值

预期结果:
  - 日志中不出现完整的原始 Secret 值
  - 若平台能检测拼接，拼接结果也被遮蔽

验证点:
  - [负向] 拼接重组后 echo 不泄露完整 Secret
  - [负向] 逐个字符拼接也不泄露

清理:      fixture
