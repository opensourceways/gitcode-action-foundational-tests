## 失败分诊 · REL-TIMEOUT-01-010 · 默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=CANCELED; 正向/run_logs contains "timeout" actual=not found

**根因初判**: 同 REL-TIMEOUT-01-007/008（job 被平台提前 cancel，非 timeout 触发）
**责任人**: 平台方 / 多方联合

**证据**:

- **Job 日志全量**:
  ```
  === JOB: reliability test job (status=CANCELED) ===
  [2026/07/23 22:39:20.453 GMT+08:00] [INFO] Job(1529981267208966144_1529981267187994631) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/450fce2f-10bf-4da6-afe7-252b7e442e8d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/450fce2f-10bf-4da6-afe7-252b7e442e8d.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发未声明 timeout-minutes 的 workflow，job 执行 sleep 21660
  - 预期结果: job 在 360 分钟时被终止; 状态为 failure; 日志含超时信息

- **实际行为**:
  - Job 未声明 `timeout-minutes`（应使用默认 360 分钟），step `sleep 21660`（361 分钟）
  - 与 TIMEOUT-007/008 完全相同的模式：job 立即 CANCELED，sleep 未实际执行
  - log 仅 5 行——无 timeout 相关信息
  - **失败传导链**: 同 TIMEOUT-007/008 → 平台 prevent long sleep → job CANCELED → 断言全部失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test`:
    ```yaml
    test:
      name: reliability test job
      runs-on: [dedicate-hosted, x64, large]
      steps:
        - name: sleep step
          run: |
            sleep 21660
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 121 行:
    默认超时时间为 360 分钟（6 小时）
  - **逐项映射**: 未声明 `timeout-minutes` → 应使用默认值 360 分钟; `sleep 21660` (361分钟) → 期望在默认 360 分后被终止。同 TIMEOUT-007/008——job 被提前 cancel 而非 timeout 触发。

- **环境前置条件验证**: runner 可用但被提前 cancel

**置信度**: 中（同 TIMEOUT-007/008 模式——所有长 sleep 测试均被阻止）

**影响**:
- **阻塞性**: 🟡中等 — 默认 timeout 行为未被验证
- **静默性**: 🟡中等 — CANCELED 明确
- **影响面**: 🔴跨用例 — 4 个 TIMEOUT 用例全部无法验证
- **综合**: 平台/环境对超长 sleep（>~几小时）有非 timeout 的全局取消机制——所有 TIMEOUT 用例的 sleep 均被提前终止
- **是否有规避手段**: 是（使用更短的 timeout-minutes 和更短的 sleep 进行时间边界测试；例如 timeout-minutes=1 + sleep 30 测试未超时场景，timeout-minutes=1 + sleep 120 测试超时场景）

**建议**:
- 4 个 TIMEOUT 用例需要重新设计：当前 sleep 值过大（21540/21660 秒），被平台级限制阻止
- 考虑缩小 sleep 到 30-300 秒范围，使用更小的 timeout-minutes（如 1 或 0.5）测试边界行为
- 确认平台 workspace 级别的最大运行时长限制
