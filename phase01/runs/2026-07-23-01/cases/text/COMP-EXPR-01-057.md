用例 ID:   COMP-EXPR-01-057
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-183~185
母意图:    —
标题:      format substring replace 函数边界行为

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 env 中使用 format 拼接字符串，使用 substring 截取 SHA，使用 replace 替换前缀
  2. 验证输出符合预期

预期结果:
  - format 按占位符替换，substring 截取指定长度，replace 替换所有匹配子串

验证点:
  - [正向] format 输出拼接后的字符串
  - [正向] substring 输出指定长度子串
  - [正向] replace 输出替换后的字符串

清理:      重置 fixture 仓库
