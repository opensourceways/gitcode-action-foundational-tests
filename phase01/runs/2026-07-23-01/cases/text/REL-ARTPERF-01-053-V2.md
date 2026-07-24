用例 ID:   REL-ARTPERF-01-053-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-053
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      制品传输性能——1GB artifact 上传下载耗时

前置条件:
  - 仓库具备 artifact 使用权限

操作步骤:
  1. 触发含 1GB artifact upload/download 的 workflow

预期结果:
  - 上传/下载均成功且 hash 100% 匹配
  - 上传≤300s 下载≤300s

验证点:
  - [正向] 上传≤300s
  - [正向] 下载≤300s
  - [正向] hash 100% 匹配

清理:      重置 fixture 仓库
