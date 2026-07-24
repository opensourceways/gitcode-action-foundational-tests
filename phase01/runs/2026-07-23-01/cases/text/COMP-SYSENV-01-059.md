用例 ID:   COMP-SYSENV-01-059
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-197~222
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      ATOMGIT 系统环境变量关键变量存在性

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 step 的 run 中输出所有 ATOMGIT_* 环境变量是否存在
  2. 运行 workflow 检查日志

预期结果:
  - ATOMGIT_SHA / REF / REF_NAME / REF_TYPE / EVENT_NAME / EVENT_PATH / WORKSPACE / REPOSITORY / RUN_ID / RUN_NUMBER / WORKFLOW / SERVER_URL / API_URL / OUTPUT / ENV / PATH / STEP_SUMMARY 均存在且非空

验证点:
  - [正向] 关键 ATOMGIT_* 变量在日志中显示非空
  - [负向] 无关键变量缺失

清理:      重置 fixture 仓库
