用例 ID:   COMP-STACKMASK-01-001
维度标签:   [completeness, security]
维度:      完备性
优先级:    P0
溯源意图:  INTENT-COMP-012
母意图:    —
标题:      secret 在错误堆栈与异常输出中必须保持脱敏

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在默认分支存在

操作步骤:
  1. 提交一个故意触发错误的 workflow，在错误路径中引用 secret
  2. 触发 workflow 并查看运行日志中的错误堆栈
  3. 检查异常输出、失败步骤的摘要中是否泄露 secret

预期结果:
  - 错误堆栈中不出现 DEPLOY_TOKEN 明文
  - 失败步骤的日志摘要中不出现 DEPLOY_TOKEN 明文
  - 系统在所有输出路径（stdout/stderr/堆栈/摘要）中保持脱敏

验证点:
  - [负向] 错误堆栈不含 DEPLOY_TOKEN 明文
  - [负向] 步骤摘要不含 DEPLOY_TOKEN 明文

清理:      fixture
