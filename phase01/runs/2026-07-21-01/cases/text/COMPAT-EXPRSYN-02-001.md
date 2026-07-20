用例 ID:   COMPAT-EXPRSYN-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-003
标题:      验证状态函数不带括号时语法等价于 GitHub success()/failure()
incorporates: TC-317~321 (条件执行函数问题)

前置条件:
  - 在 if 条件中使用 GitCode 和 GitHub 语法

操作步骤:
  1. if: ${{ success }} → 全部前置成功时执行
  2. if: ${{ failed }} → 任一前置失败时执行
  3. if: ${{ always }} → 无条件执行
  4. if: ${{ cancelled }} → 被取消时执行
  5. if: ${{ success() }}（GitHub 括号语法）→ 验证报错还是兼容
  6. if: ${{ failure() }} → 验证行为

预期结果:
  - 不带括号语法与 GitHub 括号语法语义等价
  - GitHub 括号语法应明确报错（非静默当字符串）
  - ${{ failed }} 等于 GitHub ${{ failure() }}

验证点:
  - [正向] success/failed/always/cancelled 正确求值
  - [负向] ${{ failure() }} 应有明确报错
  - [正向] ${{ success }} 可在 run: 中 echo 为 true/false

清理:      fixture
