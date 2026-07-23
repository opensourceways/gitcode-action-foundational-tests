用例 ID:   USE-CTX-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-002
母意图:    —
标题:      使用 atomgit 上下文时表达式正常求值

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 的 run 步骤中引用 ${{ atomgit.ref }}

预期结果:
  表达式正确求值为当前分支引用

验证点:
  - [正向] 日志中输出当前分支引用值
  - [正向] 运行成功完成

清理:      无

