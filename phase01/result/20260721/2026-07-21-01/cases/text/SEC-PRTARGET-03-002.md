用例 ID:   SEC-PRTARGET-03-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    —
标题:      pull_request_target 下显式 checkout fork PR head 代码后不应自动执行其中脚本

前置条件:
  - 主仓库默认分支有 pull_request_target workflow
  - fork 侧 PR 包含恶意脚本（如 echo "FORK_CODE_RUN"）
  - workflow 中显式 checkout ref: head.sha

操作步骤:
  1. pull_request_target workflow 中用 `uses: checkout` 并指定 `ref: ${{ atomgit.event.pull_request.head.sha }}`
  2. checkout 后执行 `make build` 类命令
  3. 观察 checkout step 是否产生安全警告
  4. fork 侧脚本是否被执行

预期结果:
  - 显式 checkout head.sha 时 checkout action 应产生安全警告或要求显式确认
  - 无显式 checkout ref 时不应自动获取 fork 侧代码变更
  - 显式 checkout 后的 fork 命令会被执行（作者有意识决策）

验证点:
  - [负向] 无显式 checkout ref 时不执行 fork 代码
  - [正向] 显式 checkout head.sha 时 checkout step 产生安全警告
  - [正向] checkout head.sha 后执行命令是作者有意行为

清理: fixture
