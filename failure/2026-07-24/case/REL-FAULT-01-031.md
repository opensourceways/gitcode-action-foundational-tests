## 失败分诊 · REL-FAULT-01-031 · 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains step_one_marker actual=contains(满足); 负向/run_logs expected=NOT contains step_four_marker actual=contains(违反)

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（25 行）:
  ```
  === JOB: fault injection SIGKILL (status=COMPLETED) ===
  [2026/07/23 22:28:25.487] [INFO] Job(1529978520157822976_1529978520124268551) duration check: true
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

- **预期行为**（Phase 01 文本用例 REL-FAULT-01-031，优先级 P1，维度 稳定性）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤 1: 触发 workflow，在 job 执行到第 3 个 step 时对 runner 进程注入 SIGKILL
  - 预期结果: job 状态=failure; step 1-2 的日志完整可查看; step 3 日志不完整或标记为中断

- **实际行为**:
  - job 以 COMPLETED 状态完整执行了所有 5 个 step
  - step_one_marker, step_two_marker, step_four_marker, step_five_marker 全部出现
  - step 3 (sleep 30) 也正常执行完毕
  - 故障注入（SIGKILL）完全没有生效，runner 进程未被杀死

- **对照 GitCode 规格**:
  - 无直接相关规格段落；此用例依赖 harness 的故障注入能力

- **环境前置条件验证**: harness 声称具备故障注入能力（at: mid_job, action: kill_runner, target_step: 3），但实际未生效

**置信度**: 高 (所有 step 均正常执行，SIGKILL 明显未注入)

**影响**:
- **阻塞性**: 🔴阻塞 — 故障注入能力完全缺失，无法验证 SIGKILL 场景
- **静默性**: 🔴静默错误 — 无任何故障注入失败的警告或错误日志
- **影响面**: 🔴跨维度 — 影响所有故障注入测试（REL-FAULT-01-032, REL-FAULT-01-033）
- **综合**: harness 声明的故障注入能力未实际部署或未正确触发
- **是否有规避手段**: 否（harness 需要实现实际的故障注入机制）

**建议**:
- Phase 02 排查故障注入模块是否已部署，确认 kill_runner action 的实现逻辑
- 增加故障注入执行确认日志，确保每次注入都有明确的成功/失败记录
