用例 ID:   SEC-MASK-03-005
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-027
母意图:    —
标题:      ::add-mask:: workflow 命令的正确性与安全性

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 在 workflow step 中使用 echo '::add-mask::MY_DYNAMIC_SECRET' 注册动态脱敏值
  2. 随后 echo 该动态值，观察日志中是否被遮蔽
  3. 尝试使用 ::stop-commands:: 后再 echo 该值

预期结果:
  - ::add-mask:: 注册的值在后续日志中被遮蔽为 ***
  - ::stop-commands:: 不应恢复被 mask 的值

验证点:
  - [正向] echo '::add-mask::VALUE' 后 echo VALUE，日志显示 ***
  - [负向] ::stop-commands:: 后 echo VALUE，仍应被遮蔽
  - [负向] add-mask 命令返回值不含要遮蔽的原始值

清理:      none
