用例 ID:   COMP-EXPRFN-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-013
标题:      验证表达式函数的边界行为: contains/startsWith/endsWith/format/hashFiles/toJson
前置条件:  仓库无特殊设置
操作步骤:
  1. contains('hello world', '') 空串参数
  2. startsWith('', 'prefix') 空串边界
  3. format('{0}{1}', 'a') 缺参数
  4. hashFiles('nonexistent/**') 无匹配文件
  5. toJson(atomgit.event) 复杂对象序列化
预期结果: 各函数边界行为确定，不崩溃不静默
验证点:
  - [正向] contains 对空串边界行为明确
  - [正向] startsWith/endsWith 空串边界明确
  - [正向] format 缺参数有明确处理
  - [正向] hashFiles 无匹配文件明确返回值
  - [正向] toJson 对复杂对象返回合法 JSON
清理:      fixture
