用例 ID:   COMPAT-CTX-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-016
母意图:    —
标题:      使用 github.ref 上下文应报错或求值为空

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 在 workflow 的 run 步骤中引用 ${{ github.ref }}
  2. 提交并推送该 workflow
  3. 触发 workflow 运行

预期结果:
  - 平台应对 github.* 上下文给出明确报错，或在运行时求值为空字符串
  - 不应将 github.ref 静默映射到 atomgit.ref

验证点:
  - [负向] 使用 github.ref 不应被静默映射为 atomgit.ref
  - [非功能] 报错信息应提示将 github.* 替换为 atomgit.*

清理:      fixture
