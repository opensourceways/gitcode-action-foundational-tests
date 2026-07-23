用例 ID:   SEC-REGRESS-03-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-051
母意图:    —
标题:      [回归 #66] pull_request_target 的 fork PR secret 隔离

前置条件:
  - 主仓库默认分支有 pull_request_target workflow（声明完整 permissions 和 Secret 引用）
  - fork 仓库侧修改了同路径 workflow YAML，添加了 echo secret 的恶意命令
  - 从 fork 向主仓提交 PR

操作步骤:
  1. 在 fork 侧修改 `.gitcode/workflows/pr-target.yml`，在 run 中添加 `echo "${{ secrets.DEPLOY_TOKEN }}"`
  2. 向主仓提交 fork PR 触发 pull_request_target 事件
  3. 观察实际执行的 workflow 步骤是否来自 fork 侧还是默认分支

预期结果:
  - 实际执行的 workflow 定义应来自目标仓库默认分支，不受 fork 侧修改影响
  - fork 侧添加的 echo secret 命令不应被执行
  - workflow 执行的 git SHA 应与默认分支当前版本一致

验证点:
  - [正向] 若 #66 已实现：实际执行的 workflow steps 与默认分支 YAML 一致
  - [负向] fork 侧添加的恶意 step 不应出现在执行日志中
  - [负向] 执行日志中的 workflow 版本信息（如 git SHA）应为默认分支最新 commit
  - [状态] 若 #66 仍未实现（715 开发中），本用例标记为 blocked-by-platform

清理:      fixture
