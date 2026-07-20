用例 ID:   SEC-FORK-02-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
标题:      pull_request_target 下 checkout head.sha 后不应自动信任 fork 侧代码

前置条件:
  - 目标仓库 base 分支有 pull_request_target workflow
  - fork 侧的 Makefile 包含恶意命令
  - workflow 中显式 checkout ref: head.sha 后执行 make build

操作步骤:
  1. pull_request_target workflow 中 checkout ref: ${{ atomgit.event.pull_request.head.sha }}
  2. checkout 后执行 run: make build（使用 fork 侧的 Makefile）
  3. 观察 checkout action 是否产生安全警告

预期结果:
  - checkout head.sha 后执行 make 会运行 fork 侧代码（这是作者的有意行为）
  - 但 checkout action 应产生安全警告或要求显式确认
  - 未显式 checkout ref 时不应获取 fork 侧代码

验证点:
  - [正向] 显式 checkout head.sha 后可执行 fork 侧代码
  - [负向] 不显式指定 ref 时不获取 fork 侧代码
  - [非功能] checkout action 是否存在安全提示机制

清理:      fixture
