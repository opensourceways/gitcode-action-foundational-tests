用例 ID:   COMP-ADD-MASK-03-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-026
标题:      ::add-mask:: 脱敏命令：验证后续日志中的值被正确遮蔽

前置条件:
  - step 中使用 ::add-mask:: 命令遮蔽敏感值

操作步骤:
  1. step 执行 echo "::add-mask::SECRET_VALUE_123"
  2. 后续执行 echo "SECRET_VALUE_123" 验证被替换为 ***
  3. 验证在命令输出、echo 打印中均被遮蔽

预期结果:
  - add-mask 后该值在所有日志行中被替换为 ***
  - echo 输出含被遮蔽后的内容
  - 原始值不出现在日志中

验证点:
  - [正向] 日志中原始值被 *** 遮蔽
  - [正向] 命令输出中也遮蔽
  - [负向] 原始值不出现在任何日志行

清理:      none
