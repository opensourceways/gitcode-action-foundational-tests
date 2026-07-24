## 失败分诊 · REL-TIMEOUT-01-009 · 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=CANCELED; 非功能/job_duration_seconds ≤70 actual=无法验证

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:39:09.913] [INFO] Job(1529981223072178176_1529981223042818055) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-TIMEOUT-01-009，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发 timeout-minutes=1 的 workflow，step 执行 sleep 120
  - 预期结果: job 在 60±10 秒时被终止; 状态为 failure; 日志含超时信息

- **实际行为**:
  - job 被标记为 CANCELED，无 step 执行日志
  - 此用例 timeout-minutes=1 且 sleep 120，理论上 60 秒后 platform 应触发超时
  - 但 harness 在 job 开始后立即取消了它（未等待 60 秒）
  - 相比 REL-TIMEOUT-01-007/008 的数小时，此用例仅需约 60 秒，但 harness 仍在更早阶段取消

- **对照 GitCode 规格**:
  - 同 REL-TIMEOUT-01-007

- **环境前置条件验证**: 同 REL-TIMEOUT-01-007

**置信度**: 中 (harness 取消所有 timeout 测试，但 60 秒超时的测试理论上不应被全局超时保护拦截)

**影响**:
- **阻塞性**: 🟡非阻塞 — 同 REL-TIMEOUT-01-007
- **静默性**: 🟡可察觉 — CANCELED 明确
- **影响面**: 🟡同维度 — 影响所有 timeout 测试
- **综合**: harness 可能对 timeout 测试用例做了统一取消处理（无论时长），导致 60 秒级别的短超时测试也无法执行
- **是否有规避手段**: 是（为 timeout 测试关闭 harness 的超时保护）

**建议**:
- 区分短超时（≤ 5 分钟）和长超时（> 5 分钟）测试：短超时测试应允许正常执行，长超时测试需要加速时间模拟
- 检查 harness 是否有针对 timeout 测试的特殊处理逻辑
