用例 ID:   COMPAT-ENV-INJ-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-093
标题:      env 变量注入不一致：${{ env.VAR }} vs Bash $VAR 行为差异——历史 #46/#533

前置条件:
  - job env 中定义 MY_VAR: hello
  - step 中同时用表达式和 shell 两种方式读取

操作步骤:
  1. 在 job.env 定义 MY_VAR: hello
  2. 在 step 中用 ${{ env.MY_VAR }} 读取（表达式层）
  3. 在同一 step 中用 echo $MY_VAR 读取（shell 环境层）
  4. 对比两次输出是否一致

预期结果:
  - ${{ env.MY_VAR }} 应输出 hello（表达式层正常）
  - echo $MY_VAR 也应输出 hello（shell 环境变量应被注入）
  - 若 shell 层为空：确认 TC-533 FAIL——Job env 未注入到 Shell

验证点:
  - [正向] 表达式层 ${{ env.MY_VAR }} 输出 hello
  - [正向] shell 层 $MY_VAR 输出 hello（不应为空）
  - [负向] 不应出现「表达式有值、shell 为空」的不一致

清理:      fixture
