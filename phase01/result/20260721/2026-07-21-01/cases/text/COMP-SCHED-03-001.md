用例 ID:   COMP-SCHED-03-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-005
母意图:    —
标题:      schedule cron 触发完整链路——已知 blocker（S3x24+TC-391）

前置条件:
  - 仓库默认分支有 schedule 触发 workflow
  - 配置了 cron 表达式（如 `*/5 * * * *` 每5分钟）
  - 已知 scheduler 当前不工作（S3x24+TC-391 P0 blocker）

操作步骤:
  1. 配置 cron 表达式触发 workflow
  2. 等待调度时间到达
  3. 通过 API 检查是否产生了 workflow run
  4. 检查 run 的 event_name 是否为 schedule

预期结果:
  - 按 cron 表达式在 UTC 时区触发 workflow 运行（修复后）
  - `atomgit.event_name=schedule`
  - `atomgit.event.schedule` 含 cron 表达式信息
  - cron 在默认分支上生效，最短间隔 5 分钟

验证点:
  - [正向] workflow run 列表中出现在调度时间点触发的 run（T+5min内）
  - [正向] API 返回 `event_name=schedule`
  - [正向] cron 表达式解析正确（五段式 POSIX cron）
  - [状态] 若 scheduler 仍未修复——标记为 blocked-by-platform

清理: fixture
