用例 ID:   COMP-EXPRFN-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-013
标题:      验证表达式函数边界行为 contains/startsWith/endsWith/format/hashFiles/toJson
incorporates: TC-180~187 (表达式函数)

前置条件:
  - 使用各表达式函数在边界参数下求值

操作步骤:
  1. contains 空串/单字符/多字节 UTF-8
  2. startsWith/endsWith 空串边界
  3. format 缺参数/多参数
  4. hashFiles 无匹配文件
  5. toJson 复杂对象/null/数组

预期结果:
  - 各函数边界行为一致可预测
  - 空参数/无匹配文件不导致崩溃
  - toJson 返回合法 JSON 字符串

验证点:
  - [正向] 各类输入处理正确
  - [负向] 语法错误不导致静默跳过
  - [正向] hashFiles 无匹配时行为明确

清理:      fixture
