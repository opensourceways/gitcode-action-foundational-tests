用例 ID:   COMP-STEP-01-071
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-279~288
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      step 执行控制 shell working-directory continue-on-error timeout-minutes 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 shell / working-directory / continue-on-error / timeout-minutes 的 step
  2. 验证各字段生效

预期结果:
  - shell 指定执行器，working-directory 指定执行目录，continue-on-error true 时步骤失败不终止 job，timeout-minutes 限制步骤时长

验证点:
  - [正向] shell bash 和 sh 均可执行
  - [正向] working-directory 改变执行目录
  - [正向] continue-on-error true 被接受

清理:      重置 fixture 仓库
