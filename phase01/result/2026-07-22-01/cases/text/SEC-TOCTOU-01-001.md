用例 ID:   SEC-TOCTOU-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-031
母意图:    —
标题:      审批后推送新 commit 不应绕过审批与代码固定

前置条件:
  - 仓库启用了 PR 审批机制（需人工审批后才能运行 workflow）
  - 存在一个外部 fork 的 PR

操作步骤:
  1. 外部贡献者提交一个 PR，触发需审批的 workflow
  2. 维护者审批该 PR，允许 workflow 运行
  3. 在审批通过后、workflow 执行前，外部贡献者向 PR 头部分支推送新的 commit
  4. 观察后续触发的 workflow 执行结果

预期结果:
  - 系统在审批后检测到 PR 头部 commit 发生变化时，应重新要求审批或固定审批时的 commit SHA
  - 新的 commit 不应在未经重新审批的情况下直接执行 workflow
  - 运行日志中显示的触发 SHA 应与审批时的 SHA 一致，或 workflow 被暂停等待重新审批

验证点:
  - [负向] 新 commit 未在未经重新审批的情况下执行
  - [负向] 系统未使用审批后更新的不可信代码执行 workflow
  - [正向] 系统重新触发审批流程或固定代码到审批时版本

清理:      重置 fixture 仓库
