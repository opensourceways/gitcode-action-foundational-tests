用例 ID:   SEC-EXPR-03-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-035
母意图:    —
标题:      事件负载中不可信字段在 expression evaluation 阶段的类型安全

前置条件:
  - 存在 pull_request 触发的 workflow

操作步骤:
  1. workflow 中引用 ${{ atomgit.event }} 作为整体
  2. 在 run 和 if 中使用该值
  3. 验证不导致 shell 语法错误或崩溃

预期结果:
  - 表达式求值产物不导致 shell 语法错误
  - 嵌套对象用于 if 不崩掉解析器

验证点:
  - [负向] ${{ atomgit.event }} 用于 run 不应导致 shell 语法错误
  - [负向] ${{ atomgit.event.* }} 嵌套对象用于 if 不应崩掉解析器

清理:      none
