用例 ID:   REL-RERUN-01-011
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-011
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    —
标题:      rerun 边界值——单条运行连续重新运行 3 次应全部成功

前置条件:
  - 仓库存在一次失败的 workflow 运行

操作步骤:
  1. 对该运行依次执行 Re-run all jobs 共 3 次

预期结果:
  - 第 1-3 次 rerun 均创建新运行
  - 每次 rerun 的 atomgit.sha/ref 与原始运行一致
  - 3 次新运行均 success

验证点:
  - [正向] 运行编号递增
  - [正向] 每次 rerun 状态=success
  - [负向] 不应复用旧运行记录

清理:      无需特殊清理
