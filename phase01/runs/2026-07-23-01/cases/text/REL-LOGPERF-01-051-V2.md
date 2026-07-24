用例 ID:   REL-LOGPERF-01-051-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-051
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    —
标题:      日志加载性能——200MB 日志下载与查看耗时

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. 触发生成 200MB 日志的 workflow，测量下载与查看耗时

预期结果:
  - 200MB 日志可在 ≤120s 内下载完成
  - 日志内容完整

验证点:
  - [正向] 下载≤120s
  - [正向] 大小/行数 100% 一致

清理:      无需特殊清理
