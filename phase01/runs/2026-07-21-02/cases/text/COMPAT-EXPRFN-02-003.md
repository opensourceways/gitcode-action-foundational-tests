用例 ID:   COMPAT-EXPRFN-02-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-067
标题:      表达式函数 substring/replace/toJson 边界行为——越界、全局/首匹配、JSON 输出格式是否与 GitHub 对齐

前置条件:
  - 工作流可在 push 事件下触发

操作步骤:
  1. 在 step 中分别测试以下边界表达式：
     - substring('hello', 0, 7) / substring('hello', 10, 3) / substring('hello', -1, 2)
     - replace('aaa', 'a', 'b') / replace('a/a', '/', '-') / replace('abc', '', 'x')
     - toJson(atomgit.event) / toJson(null) / toJson(true)
  2. 记录各函数输出结果，与 GitHub toJSON 行为或预期行为比对

预期结果:
  - substring 越界时安全截断，不报错
  - replace 行为明确（全局或首个匹配），空串 old 有确定处理
  - toJson 输出为 pretty-print、合法 JSON，可被标准 JSON 解析器消费

验证点:
  - [正向] substring('hello', 0, 7) 输出 hello（越界安全截断）
  - [正向] replace('aaa', 'a', 'b') 行为被明确记录（全局 bbb 或首个 baa）
  - [正向] toJson(atomgit.event) 输出为 pretty-print、合法 JSON
  - [负向] substring('hello', 0, 7) 不应报错导致表达式解析失败
  - [负向] replace('a/a', '/', '-') 若文档未声明全局/首个，实测结果应被记录为权威行为
  - [非功能] substring/replace 边界行为（越界、空 old、负索引）应文档化，消除黑盒状态

清理:      fixture
