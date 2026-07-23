用例 ID:   SEC-EXPR-01-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-035
标题:      事件负载不可信字段在 expression evaluation 阶段的类型安全

前置条件:
  - 仓库有 PR 触发的 workflow
  - workflow 使用 ${{ atomgit.event.* }} 表达式
  - 已有用例 TC-033 发现 atomgit.event 返回对象字面量导致 shell 语法错误

操作步骤:
  1. 在 run: 中直接使用 ${{ atomgit.event }} → 验证不导致 shell 语法错误
  2. 在 if: 条件中使用嵌套对象字段 → 验证解析器不崩溃
  3. 使用 ${{ toJSON(atomgit.event) }}（若支持）→ 验证返回合法 JSON
  4. 构造含特殊字符的 PR 标题/正文，观察表达式求值结果
  5. 验证 expression evaluation 产物在替换后安全

预期结果:
  - expression evaluation 产物替换后不导致 shell 语法错误
  - 对象/数组类型在替换时被安全序列化
  - 不出现因类型不匹配导致语法错误（如 TC-033 的 "unexpected token '('"）
  - 若无法安全替换，前置 lint/parse 阶段应报错

验证点:
  - [负向] ${{ atomgit.event }} 用于 run 不导致 shell 语法错误
  - [负向] 嵌套字段在 if 条件中不崩解析器
  - [正向] 类型转换行为一致且可预测
  - [负向] 不出现 TC-033 类型的对象字面量注入问题

清理:      fixture
