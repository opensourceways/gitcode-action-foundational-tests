## 失败分诊 · REL-TIMEOUT-01-008 · job timeout 越界触发——361 分钟应在 360 分钟被强制终止

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=CANCELED; 正向/run_logs contains "timeout" actual=not found

**根因初判**: 同 REL-TIMEOUT-01-007（job 被平台提前 cancel，非 timeout 触发）
**责任人**: 平台方 / 多方联合

**证据**:

- **Job 日志全量**:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:58.894 GMT+08:00] [INFO] Job(1529981176968261632_1529981176947290119) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21660
  - 预期结果: job 在 360±2 分钟时被终止; 状态为 failure; 日志含超时信息

- **实际行为**:
  - Job 设置了 `timeout-minutes: 360`，step 是 `sleep 21660`（361 分钟）
  - Job 立即被标记为 CANCELED（非 failure），sleep 未实际执行
  - log 仅到 `Executing: bash -e ...`——无 timeout 信息
  - 同 REL-TIMEOUT-01-007——平台/环境层面不允许超长 sleep
  - **失败传导链**: 平台提前 cancel → CANCELED 非 failure → timeout 日志不存在 → 断言全部失败

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
            sleep 21660
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
    超时后 job 将被强制终止
  - **逐项映射**: `timeout-minutes: 360` + `sleep 21660` (361分钟期望超时) → 匹配规格; 但 job 被提前 cancel（非 timeout-minutes 触发）。与 TIMEOUT-007 相同平台限制问题。

- **环境前置条件验证**: 同 REL-TIMEOUT-01-007——runner 可用但被提前 cancel

**置信度**: 中（与 TIMEOUT-007 相同模式——平台/环境阻止超长运行）

**影响**:
- **阻塞性**: 🟡中等 — timeout 越界行为未被验证
- **静默性**: 🟡中等 — CANCELED 明确但原因不明
- **影响面**: 🔴跨用例 — 与 TIMEOUT-007/009/010 共享相同根因
- **综合**: 所有 4 个 TIMEOUT 用例均被平台级限制阻止——无法验证 timeout-minutes 边界行为
- **是否有规避手段**: 是（确认平台级运行时长限制；使用更短的 timeout-minutes 如 5 分钟和 3 分钟 sleep 来测试边界）

**建议**:
- 与 REL-TIMEOUT-01-007 合并排查
- 考虑使用小 timeout（如 timeout-minutes=1, sleep 120）测试边界行为，避免触发平台级全局限制
