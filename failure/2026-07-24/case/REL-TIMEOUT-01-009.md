## 失败分诊 · REL-TIMEOUT-01-009 · 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=CANCELED; 非功能/job_duration_seconds le=70 actual=N/A

**根因初判**: 平台缺陷（CANCELED 替代了 failure——可能是 timeout 触发但状态语义与预期不符）
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:39:09.913 GMT+08:00] [INFO] Job(1529981223072178176_1529981223042818055) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发 timeout-minutes=1 的 workflow，step 执行 sleep 120
  - 预期结果: job 在 60±10 秒时被终止; 状态为 failure

- **实际行为**:
  - Job 设置了 `timeout-minutes: 1`，step 是 `sleep 120`
  - Job status=CANCELED（非 failure），但 log 被截断——仅到 `Executing: bash -e ...`
  - 如果是 timeout-minutes=1 触发，job 应该在 sleep 120 约 60 秒后终止——但日志过于简短无法确认
  - 即使 timeout 正确触发，平台返回的状态是 CANCELED 而非 failure（与断言期望不符）
  - **失败传导链**: job 被 cancel（可能是 timeout 触发）→ status=CANCELED（非 failure）→ 断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test`:
    ```yaml
    test:
      name: timeout test job
      runs-on: [dedicate-hosted, x64, large]
      timeout-minutes: 1
      steps:
        - name: long sleep step
          run: |
            sleep 120
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 110-121 行:
    ```yaml
    timeout-minutes: 30
    ```
    超时后 job 将被强制终止
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 121 行:
    默认超时时间为 360 分钟（6 小时）
  - **逐项映射**: `timeout-minutes: 1` → 匹配规格（自定义超时）; `sleep 120` → 超出 1 分钟限制应触发 timeout。测试 YAML 正确。但超时后 job 状态为 CANCELED——规格未明确定义 timeout 触发的 job 状态标签（failure 还是 canceled）。

- **环境前置条件验证**: runner 可用，但 log 过于简短——无法判断 job 实际运行了多久

**置信度**: 中（CANCELED 状态可能是 timeout 触发的正确结果，但断言期望 failure——这是平台状态语义定义问题）

**影响**:
- **阻塞性**: 🟢不阻塞 — timeout 机制可能正在正确工作（如果 CANCELED=timeout triggered）
- **静默性**: 🟡中等 — CANCELED 无详细 reason
- **影响面**: 🟡同规范 — 影响所有 timeout 相关断言
- **综合**: 平台 timeout 触发后 job 状态为 CANCELED 而非 failure——需要确认这是平台设计意图还是缺陷
- **是否有规避手段**: 是（将断言从 `equals: "failure"` 改为 `equals: "CANCELED"` 或 `in: ["failure", "CANCELED"]`）

**建议**:
- 确认平台 timeout 触发后的 job status 语义：是否总是 CANCELED
- 如果 CANCELED 是 timeout 的正确状态，更新所有 timeout 用例的断言
- 增加 timeout 的 log 验证（如检查是否有 "timeout" 相关日志输出）
