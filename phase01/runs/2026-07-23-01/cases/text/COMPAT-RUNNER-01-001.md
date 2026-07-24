用例 ID:   COMPAT-RUNNER-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-018
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      runner.os 在 Linux Runner 上应返回 Linux

前置条件:
  - 仓库已启用 Actions
  - 存在 Linux 标签的 Runner

操作步骤:
  1. 在 workflow 的 run 步骤中输出 ${{ runner.os }}
  2. 触发 workflow 运行

预期结果:
  - runner.os 应返回 Linux（首字母大写，与 GitHub 一致）

验证点:
  - [正向] 日志中 runner.os 的值为 Linux
  - [负向] 不应返回小写的 linux

清理:      fixture
