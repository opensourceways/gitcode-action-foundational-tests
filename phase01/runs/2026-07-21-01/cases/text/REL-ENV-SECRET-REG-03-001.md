用例 ID:   REL-ENV-SECRET-REG-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-048
标题:      同一 secret 两次引用不报 bad substitution——历史 #11 回归

前置条件:
  - 仓库配置 secret MY_TOKEN
  - 两个相邻 step 各自 echo 该 secret

操作步骤:
  1. step1: echo ${{ secrets.MY_TOKEN }}（第一次引用）
  2. step2: echo ${{ secrets.MY_TOKEN }}（第二次引用）
  3. 观察 step2 是否报 bad substitution

预期结果:
  - step1 和 step2 均正常 dereference secret 值
  - step2 不报 'bad substitution'
  - 两次引用值一致

验证点:
  - [正向] step1 和 step2 均 success
  - [负向] step2 不报 'bad substitution'
  - [正向] 两次日志均正常显示脱敏后的 secret

清理:      fixture
