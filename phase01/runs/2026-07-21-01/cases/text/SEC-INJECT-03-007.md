用例 ID:   SEC-INJECT-03-007
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-040
母意图:    —
标题:      表达式双重求值——action 内部模板引擎不应二次解释 ${{ }} 的结果

前置条件:
  - 存在 pull_request 触发的 workflow
  - fork 贡献者可控制 PR 标题内容

操作步骤:
  1. 在 PR 标题中放入 {{ process.env }} 等模板语法
  2. workflow 通过 ${{ }} 求值后传给 action 的 with 参数
  3. 观察 action 内部是否对参数进行二次模板插值

预期结果:
  - action 内部不应将 ${{ }} 求值结果进行二次模板解释
  - 传入 action with 参数的值应作为纯数据
  - workflow 不因模板注入异常退出

验证点:
  - [负向] action 内部不应将 with 传入的 '{{ process.env }}' 解释为模板变量
  - [负向] 日志输出不含二次插值产生的内容
  - [正向] workflow 正常完成或不因模板注入崩溃

清理:      fixture
