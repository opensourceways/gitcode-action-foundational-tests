用例 ID:   SEC-DOUBLEEVAL-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-013
母意图:    —
标题:      表达式求值应防止通过环境变量间接二次求值

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，先将包含表达式的字符串写入 env，再在后续步骤中通过 shell 展开该 env
  2. 触发该 workflow 并查看运行日志

预期结果:
  - 环境变量的值仅被求值一次，后续 shell 展开时不会再次触发模板引擎解析
  - 二次求值不应导致 secret 值被解析并输出到日志
  - 运行日志中不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [负向] 环境变量中的表达式字符串未在后续步骤中被二次解析
  - [正向] workflow 被阻止或按单级求值执行

清理:      重置 fixture 仓库
