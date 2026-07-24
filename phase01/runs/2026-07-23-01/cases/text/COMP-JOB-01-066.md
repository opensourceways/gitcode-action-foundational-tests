用例 ID:   COMP-JOB-01-066
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-264~288
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      job 必填字段 name runs-on steps 验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 name / runs-on / steps 的 job
  2. 验证缺任一字段时平台拒绝

预期结果:
  - job 必须包含 name / runs-on / steps，缺 name 时报空值错误，缺 runs-on 或 steps 时平台拒绝

验证点:
  - [正向] 完整 job 定义通过校验并执行
  - [负向] 缺 name 被平台拒绝
  - [负向] 缺 steps 被平台拒绝

清理:      重置 fixture 仓库
