用例 ID:   SEC-DOUBLEEVAL-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-013
母意图:    —
标题:      表达式求值应防止双重模板渲染（嵌套表达式）

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中故意构造嵌套表达式 ${{ ${{ secrets.DEPLOY_TOKEN }} }}
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 系统对嵌套表达式仅求值一次，或将其视为语法错误拒绝执行
  - 二次求值不应导致 secret 值被解析并输出到日志
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [负向] 系统未对表达式进行二次模板渲染
  - [正向] workflow 被阻止或按单级求值执行

清理:      重置 fixture 仓库
