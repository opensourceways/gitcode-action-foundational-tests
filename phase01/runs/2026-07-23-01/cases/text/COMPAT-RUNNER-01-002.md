用例 ID:   COMPAT-RUNNER-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-019
母意图:    —
标题:      runner.arch 在 x86_64 Runner 上应返回 X64

前置条件:
  - 仓库已启用 Actions
  - 存在 x64 标签的 Runner

操作步骤:
  1. 在 workflow 的 run 步骤中输出 ${{ runner.arch }}
  2. 触发 workflow 运行

预期结果:
  - runner.arch 应返回 X64（与 GitHub 一致）

验证点:
  - [正向] 日志中 runner.arch 的值为 X64
  - [负向] 不应返回 x86_64

清理:      fixture
