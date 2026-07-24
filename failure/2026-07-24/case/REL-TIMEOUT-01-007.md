## 失败分诊 · REL-TIMEOUT-01-007 · job timeout 边界值——359 分钟运行应在 360 分钟边界前完成

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=success actual=CANCELED; 非功能/job_duration_minutes le=359 actual=N/A

**根因初判**: 平台缺陷（job 在开始阶段即被取消——非超时触发，而是 CI 平台主动cancel）
**责任人**: 平台方 / 多方联合

**证据**:

- **Job 日志全量**:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:47.849 GMT+08:00] [INFO] Job(1529981130642173952_1529981130621202439) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21540
  - 预期结果: job 在 359 分钟前成功完成; 状态为 success

- **实际行为**:
  - Job 设置了 `timeout-minutes: 360`，step 是 `sleep 21540`（359 分钟）
  - 但 job 在 `sleep 21540` 开始后即被标记为 CANCELED——运行时长远未达到 359 分钟
  - log 仅到 `Executing: bash -e ...` 行即终止，无 `sleep` 执行输出
  - 此取消非 timeout-minutes 触发（360 分钟远未到），而是 CI 平台或 test harness 主动 cancel
  - **失败传导链**: job 被提前 cancel（非 timeout）→ job_status=CANCELED → 断言全不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test`:
    ```yaml
    test:
      name: timeout test job
      runs-on: [dedicate-hosted, x64, large]
      timeout-minutes: 360
      steps:
        - name: long sleep step
          run: |
            sleep 21540
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 110-121 行:
    ```yaml
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        timeout-minutes: 30
        steps:
          - run: ./build.sh
    ```
    默认超时时间为 360 分钟（6 小时）。超时后 job 将被强制终止。
  - **逐项映射**: `timeout-minutes: 360` → 匹配规格（默认值）; `sleep 21540` (359分钟) → 应在此届内完成; `runs-on: dedicate-hosted, x64, large` → 可执行长任务。测试 YAML 与规格一致，但 job 被提前 cancel 非 timeout-minutes 机制触发。

- **环境前置条件验证**: runner 可用但 job 被外部 cancel——可能是 CI 平台对超长运行 job 的全局限制（例如 workspace-level 或 project-level 最大运行时间 < 360 分钟）

**置信度**: 中（CANCELED 状态明确但 cancel 来源不确定——可能是平台全局限制、test harness 超时、或 runner 维护窗口）

**影响**:
- **阻塞性**: 🟡中等 — timeout-minutes 边界行为未被验证
- **静默性**: 🟡中等 — CANCELED 状态明确但原因不明
- **影响面**: 🟡同用例 — 仅影响 timeout 边界用例
- **综合**: sleep 21540（359分钟）未被允许执行——可能存在平台级或项目级的运行时长上限 < 360 分钟
- **是否有规避手段**: 是（确认平台是否有比 360 分钟更低的全局 timeout 限制；减小 sleep 时长测试更短的 timeout 边界）

**建议**:
- 确认 CI 平台是否有 project-level 或 workspace-level 的 maximum job duration 限制
- 若平台全局限制 < 360 分钟，则此用例无法按设计验证——需调整 timeout-minutes 阈值
- 检查 test harness 是否有针对长运行 job 的自动 cancel 机制
