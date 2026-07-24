用例 ID:   REL-API-01-065
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-065
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据

前置条件:
  - 具备 API 查询权限与测试脚本环境

操作步骤:
  1. 以 10 QPS 连续查询一个 running 状态的 run 详情 API，持续 60s

预期结果:
  - 全部返回 200
  - status 字段无矛盾
  - P95 响应时间≤2s

验证点:
  - [正向] 200 占比=100%
  - [负向] 不应出现 429/503/500
  - [非功能] P95≤2s

清理:      无需特殊清理
