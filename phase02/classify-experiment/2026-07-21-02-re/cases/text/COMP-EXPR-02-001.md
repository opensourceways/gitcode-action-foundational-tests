用例 ID:   COMP-EXPR-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-012
标题:      验证表达式状态函数不带括号语法 success/always/failed/cancelled
incorporates: TC-317~321 (条件执行函数问题), TC-176~179 (状态函数)

前置条件:
  - 配置 `if: ${{ success }}` / `if: ${{ always }}` / `if: ${{ failed }}` / `if: ${{ cancelled }}`

操作步骤:
  1. `if: ${{ success }}` → 全部前置成功时执行
  2. `if: ${{ always }}` → 无条件执行
  3. `if: ${{ failed }}` → 前置失败时执行
  4. `if: ${{ cancelled }}` → 取消时执行
  5. 验证 `${{ success() }}`（GitHub 语法）行为

预期结果:
  - 不带括号语法正确求值
  - GitHub 括号语法应报错或语义一致

验证点:
  - [正向] success/always/failed/cancelled 正确求值
  - [负向] ${{ success() }} 不应静默当字符串

清理:      fixture
