## 失败分诊 · REL-FAULT-01-031 · 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs contains "step_one_marker" actual=found; 负向/run_logs contains "step_four_marker" actual=found(step_four_marker 出现在日志中)

**根因初判**: 环境/Harness（故障注入未生效——SIGKILL 未被注入或注入后 runner 快速恢复）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: fault injection SIGKILL (status=COMPLETED) ===
  [2026/07/23 22:28:25.487 GMT+08:00] [INFO] Job(1529978520157822976_1529978520124268551) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/19155db2-7af6-4510-b96f-d97cab632ffa.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/19155db2-7af6-4510-b96f-d97cab632ffa.sh
  step_one_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/5facc260-54cf-47de-aec2-472fe5d04f45.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/5facc260-54cf-47de-aec2-472fe5d04f45.sh
  step_two_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e0b6526d-f857-4b0c-81ce-e4d239df2596.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e0b6526d-f857-4b0c-81ce-e4d239df2596.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/814d2183-2200-4e74-ba82-cf63d7ab8243.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/814d2183-2200-4e74-ba82-cf63d7ab8243.sh
  step_four_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1d286a0d-7419-4fbc-b3fc-233882a2c14e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1d286a0d-7419-4fbc-b3fc-233882a2c14e.sh
  step_five_marker
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤: 触发 workflow，在 job 执行到第 3 个 step 时对 runner 进程注入 SIGKILL
  - 预期结果: job 状态=failure; step 1-2 的日志完整; step 3 日志不完整或标记为中断

- **实际行为**:
  - 所有 5 个 step（1-5）全部成功执行并输出 marker，status=COMPLETED
  - step 3（sleep 30）实际未输出内容但正常完成后进入 step 4、5
  - 说明故障注入（SIGKILL to runner at step 3）完全未生效——runner 进程未被 kill
  - **失败传导链**: fault injection 未生效 → job 正常完成 → job_status=COMPLETED → 断言 job_status=failure 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 steps:
    ```yaml
    - name: step one
      run: |
        echo step_one_marker
    - name: step two
      run: |
        echo step_two_marker
    - name: step three
      run: |
        sleep 30
    - name: step four
      run: |
        echo step_four_marker
    - name: step five
      run: |
        echo step_five_marker
    ```
  - **测试 YAML** 中 fault_injection:
    ```yaml
    fault_injection:
      at: mid_job
      action: kill_runner
      params:
        target_step: 3
      recovery_expectation: retry_and_succeed
    ```
  - **GitCode 规格** `runner-management/using-hosted-runners.md` — runner 生命周期管理
  - **逐项映射**: 5-step job 结构正确; fault_injection 配置合理（mid_job/kill_runner/target_step:3）。但 killer_runner 动作未生效——这可能是因为 runner 是通过 API 调度的托管 runner（dedicate-hosted），test harness 注入的 SIGKILL 可能是发送给了 API server 而非底层 runner 进程。

- **环境前置条件验证**: runner 可用，所有 steps 正常执行；test harness 的 fault injection 机制未能在 runner 端生效

**置信度**: 高（所有 5 个 step 均成功执行，明确表明故障注入未生效——非平台问题，是 test harness 注入机制问题）

**影响**:
- **阻塞性**: 🟢不阻塞 — 故障注入机制需要修复，但不影响正常功能测试
- **静默性**: 🟡中等 — job 静默成功，无任何 fault 提示
- **影响面**: 🟡同机制 — 影响所有依赖 fault_injection 的用例
- **综合**: test harness 的 kill_runner 注入未对托管 runner 生效，可能需要使用不同的注入方式（如 runner 内部信号、step 超时取消等）
- **是否有规避手段**: 是（确认测试环境的 fault injection 机制；考虑用 step timeout 替代进程 SIGKILL 模拟）

**建议**:
- 排查 test harness 的 `kill_runner` 实现：对 dedicate-hosted（非 self-hosted）runner 如何发送 SIGKILL
- 考虑替代故障模拟方式：step 级别的 timeout/cancel 或 runner-side 信号注入
- 检查 runner 是否在 run 模式下有信号屏蔽/忽略机制
