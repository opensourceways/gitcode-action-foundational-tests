用例 ID:   COMP-STEP-01-070
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-279~288
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      step 可选字段 id env if with 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 id / env / if / with 的 step
  2. 验证各字段生效

预期结果:
  - id 用于后续引用 outputs，env 仅对该 step 生效，if 控制步骤执行，with 向 Action 传参

验证点:
  - [正向] id 定义的步骤可被后续引用 outputs
  - [正向] env 仅在该 step 内生效
  - [正向] if 条件正确控制步骤执行

清理:      重置 fixture 仓库
