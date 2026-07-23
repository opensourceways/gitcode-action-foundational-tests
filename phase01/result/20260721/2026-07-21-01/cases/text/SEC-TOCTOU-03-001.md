用例 ID:   SEC-TOCTOU-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-037
母意图:    —
标题:      pull_request_target 的 TOCTOU 攻击——审批后恶意 commit 替换 PR 代码

前置条件:
  - 目标仓库配置了 pull_request_target workflow
  - workflow 中 checkout head.sha
  - 攻击者在 PR 审批后、workflow 执行前推送恶意 commit

操作步骤:
  1. 提交无害 PR，等待审批通过
  2. 审批通过后立即推送恶意 commit（在 workflow 实际执行之前）
  3. 触发 pull_request_target workflow
  4. 验证实际执行的是审批时的 commit 还是新推送的恶意 commit

预期结果:
  - workflow 执行的代码应与审批时的 commit 一致
  - head.sha 不应自动更新为攻击者新推送的 commit
  - 仅默认分支的 workflow 版本被执行

验证点:
  - [负向] job 日志中 checkout 的 git SHA 应等于审批时锁定的 commit，非攻击者后推送的 commit
  - [正向] 未显式指定 ref 时 checkout base 分支（默认行为）——天然免疫 TOCTOU
  - [负向] head.sha 在 pull_request_target 执行时不应自动更新

清理: fixture
