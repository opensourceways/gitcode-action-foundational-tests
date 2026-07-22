用例 ID:   COMPAT-EXPRFN-02-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-066
标题:      表达式函数 format 边界行为——参数不足/过剩、转义、非字符串参数处理是否与 GitHub 一致

前置条件:
  - 工作流可在 push 事件下触发

操作步骤:
  1. 在 step 中分别使用以下 format 边界表达式并输出结果：
     - 正常替换：format('A{0}B{1}C', 'x', 'y')
     - 参数不足：format('A{0}B{1}C', 'x')
     - 参数过剩：format('A{0}B', 'x', 'y')
     - 双花括号转义：format('{{ {0} }}', 'x')
     - 非字符串参数：format('{0}', 42)、format('{0}', null)、format('{0}', true)
  2. 比对输出结果与 GitHub Actions 预期行为是否一致

预期结果:
  - 正常替换输出 AxByC
  - 参数不足时未匹配占位符原样保留，不报错（输出 AxB{1}C）
  - 参数过剩时多余参数被忽略，不报错（输出 AxB）
  - 双花括号转义为单花括号（输出 { x }）
  - 非字符串参数被隐式转字符串后插入，不导致表达式解析失败

验证点:
  - [正向] format('A{0}B{1}C', 'x', 'y') 输出 AxByC
  - [正向] format('{{ {0} }}', 'x') 输出 { x }
  - [负向] format('A{0}B{1}C', 'x') 不应报错，应输出 AxB{1}C
  - [负向] format('A{0}B', 'x', 'y') 不应因参数过剩而报错，应输出 AxB
  - [非功能] 非字符串参数（数字 42、null、true）应被转字符串插入，不导致表达式解析失败

清理:      fixture
