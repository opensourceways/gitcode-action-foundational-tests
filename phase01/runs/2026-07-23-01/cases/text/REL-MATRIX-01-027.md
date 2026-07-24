用例 ID:   REL-MATRIX-01-027
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-027
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      matrix max-parallel=4——9 个组合应最多同时运行 4 个

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发含 3x3 matrix 且 max-parallel=4 的 workflow

预期结果:
  - 任意时刻 in_progress 的 matrix job 数 ≤4
  - 前 4 个完成后自动启动后续 jobs

验证点:
  - [正向] 峰值并发≤4
  - [正向] 9 个 jobs 全部 completed(success)
  - [负向] 不应超过 4 个同时运行

清理:      无需特殊清理
