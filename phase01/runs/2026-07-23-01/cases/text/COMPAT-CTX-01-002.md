用例 ID:   COMPAT-CTX-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-016
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    COMPAT-CTX-01-001
标题:      使用 atomgit.ref 上下文应正确返回触发引用

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 的 run 步骤中引用 ${{ atomgit.ref }}
  2. 提交并推送该 workflow
  3. 触发 workflow 运行

预期结果:
  - atomgit.ref 应正确返回触发事件的引用（如 refs/heads/main）

验证点:
  - [正向] 日志中 atomgit_ref 的值不为空且符合预期格式

清理:      fixture
