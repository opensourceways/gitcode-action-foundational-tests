用例 ID:   COMPAT-EXPRBR-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-003
标题:      状态函数括号语法差异：success/failed 不带括号的语义等价

前置条件:
  - 仓库有正常 workflow 配置
  - 了解 GitCode 用 success（无括号），GitHub 用 success()（有括号）

操作步骤:
  1. 配置 if: ${{ success }} → 验证前置成功时执行
  2. 配置 if: ${{ failed }} → 验证前置失败时执行
  3. 配置 if: ${{ always }} → 验证无论如何都执行
  4. 配置 if: ${{ cancelled }} → 验证取消时执行
  5. 在 run: 中使用 ${{ success }} 作为 echo 输出 → 验证输出 true/false
  6. 配置 if: ${{ success() }}（GitHub 语法）→ 验证报错而非静默

预期结果:
  - success/failed/always/cancelled 无括号语法语义正确
  - ${{ success }} 作为表达式值输出 true/false
  - ${{ success() }}（GitHub 带括号语法）有明确报错
  - 语义等价于 GitHub 对应函数

验证点:
  - [正向] success 在成功场景执行
  - [正向] failed 在失败场景执行
  - [正向] always 始终执行
  - [负向] success() GitHub 语法应报错

清理:      fixture
