用例 ID:   REL-API-01-014
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-065
母意图:    —
标题:      API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据

前置条件:
  - 仓库已启用 Actions 且存在至少 1 个已完成或运行中的 workflow run
  - 具备以 10 QPS 频率调用 GitCode Actions API 的能力

操作步骤:
  1. 获取当前仓库的 run 列表，记录 total_count 与若干 run 的详情
  2. 以 10 QPS 的频率连续调用以下 API 30 秒（约 300 次请求）：
     - GET /api/v8/repos/:owner/:repo/actions/runs
     - GET /api/v8/repos/:owner/:repo/actions/runs/:run_id
     - GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs
  3. 观察是否有 429 限流响应或 5xx 错误
  4. 比对高频查询前后的数据一致性（run 数量、状态、字段值）

预期结果:
  - 所有请求的响应数据一致，不出现数据丢失或状态跳跃
  - 若触发限流，应返回 429 状态码，而非 500 或数据损坏
  - run/job 字段值（status、start_time、end_time 等）在查询期间保持稳定（终态运行不突变）

验证点:
  - [正向] 响应数据前后一致，无字段丢失
  - [负向] 不出现 5xx 错误
  - [正向] 若限流，返回 429 且包含 Retry-After 头

清理:      无（只读操作）
