用例 ID:   COMP-SYSENV-01-060
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-197~222
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      ATOMGIT 系统环境变量值正确性

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 step 中比对 ATOMGIT_* 环境变量与 atomgit 上下文值的一致性
  2. 验证各变量值格式正确

预期结果:
  - ATOMGIT_SHA 与 atomgit.sha 一致，ATOMGIT_REF 与 atomgit.ref 一致，ATOMGIT_EVENT_NAME 与 atomgit.event_name 一致

验证点:
  - [正向] ATOMGIT_SHA 等于 atomgit.sha
  - [正向] ATOMGIT_REF 等于 atomgit.ref
  - [正向] ATOMGIT_RUN_NUMBER 与 atomgit.run_number 一致

清理:      重置 fixture 仓库
