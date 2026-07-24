用例 ID:   COMP-ENVCTX-01-050
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-001~004
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      env 优先级链 step 大于 job 大于 workflow

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 workflow / job / step 三级定义同名 env 变量
  2. 在 step 中输出该变量值验证优先级

预期结果:
  - step 级 env 覆盖 job 级，job 级覆盖 workflow 级

验证点:
  - [正向] 最终输出值为 step 级定义的值
  - [正向] 无 job 级 env 时继承 workflow 级

清理:      重置 fixture 仓库
