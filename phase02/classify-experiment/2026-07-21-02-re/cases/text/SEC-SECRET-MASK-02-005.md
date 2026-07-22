用例 ID:   SEC-SECRET-MASK-02-005
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-027
标题:      ::add-mask:: 命令的正确性与安全性

前置条件:
  - workflow 中使用 ::add-mask:: 动态注册遮蔽值

操作步骤:
  1. `echo '::add-mask::MY_DYNAMIC_SECRET'`
  2. `echo MY_DYNAMIC_SECRET` — 验证遮蔽
  3. 不同 step 多次注册不同值，验证互不干扰

预期结果:
  - 注册后的值在日志中被遮蔽
  - 不同 step 的 mask 不互相覆盖或泄露

验证点:
  - [正向] add-mask 注册后 echo 注册值显示 ***
  - [负向] ::stop-commands:: 不恢复已注册 mask
  - [负向] 不同 step mask 表独立

清理:      fixture
