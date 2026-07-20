用例 ID:   COMP-EXPR-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-012
标题:      验证表达式状态函数不带括号的语法: success/always/failed/cancelled
前置条件:  仓库无特殊设置
操作步骤:
  1. 使用 if: ${{ success }} 在全部前置成功时执行 step
  2. 使用 if: ${{ always }} 无条件执行
  3. 使用 if: ${{ failed }} 在前置失败时触发
  4. 使用 if: ${{ cancelled }} 在 workflow 取消时触发
  5. 尝试 GitHub 语法 if: ${{ success() }} 观察行为
预期结果: GitCode 状态函数不带括号语义正确；${{ success() }} 应有明确行为
验证点:
  - [正向] ${{ success }} 不带括号正确求值
  - [正向] ${{ always }} 无条件触发
  - [正向] ${{ failed }} 前置失败时正确触发
  - [负向] ${{ success() }} 带括号应有明确报错或行为
清理:      fixture
