用例 ID:   COMP-STEP-01-069
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-279~288
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      step 必填与核心字段 name run uses 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 name / run 的 step 和含 name / uses 的 step
  2. 验证 step name 必填且无非法字符

预期结果:
  - 每个 step 必须有 name，run 执行 shell 命令，uses 调用 Action，name 不含非法字符

验证点:
  - [正向] name + run 步骤正常执行
  - [正向] name + uses 步骤正常执行
  - [负向] step name 含非法字符被拒绝

清理:      重置 fixture 仓库
