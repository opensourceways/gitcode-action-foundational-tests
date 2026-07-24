## 失败分诊 · REL-CONTINUE-01-030 · continue-on-error=true——job 失败后 workflow 不应终止

**判定结果**: FAIL
**失败断言**: 正向/job_a_status expected=failure actual=FAILED(一致); 正向/job_b_status expected=success actual=COMPLETED(一致); 正向/workflow_status expected=success actual=FAILED(推测)

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（14 行）:
  ```
  === JOB: job with continue on error (status=FAILED) ===
  [2026/07/23 22:27:31.993] [INFO] Job(1529978295787597824_1529978295762432000) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/61339c12-85ba-4342-a369-a969479bacf5.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/61339c12-85ba-4342-a369-a969479bacf5.sh
  ::error::Process exited with code 1

  === JOB: downstream after continue (status=COMPLETED) ===
  [2026/07/23 22:27:31.995] [INFO] Job(1529978295787597824_1529978295762432002) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/86eba7bd-0f4b-41b2-ac4f-c0f19e468184.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/86eba7bd-0f4b-41b2-ac4f-c0f19e468184.sh
  job_b executed
  ```

- **预期行为**（Phase 01 文本用例 REL-CONTINUE-01-030，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发含 continue-on-error=true 的失败 job 和下游 job 的 workflow
  - 预期结果: job_a 状态=failure 但 workflow 不终止; job_b 正常执行并 success

- **实际行为**:
  - job_a 正确失败（exit 1），状态 FAILED
  - job_b 正常执行，输出 "job_b executed"，状态 COMPLETED
  - job_a 和 job_b 的行为完全符合预期
  - 但整体测试仍判定为 FAIL，说明 `workflow_status` 断言失败：尽管 continue-on-error=true 且 job_b 成功，workflow 整体状态可能仍被 platform 标记为 failure

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 无直接相关规格段落；continue-on-error 应使 workflow 在 job 失败时继续运行且整体标记为 success

- **环境前置条件验证**: runner 可用，两个 job 均正确调度执行

**置信度**: 高 (job 层面行为完全符合预期，问题在于 platform 对 workflow 整体状态的判定)

**影响**:
- **阻塞性**: 🔴阻塞 — continue-on-error 语义未正确实现，影响所有依赖此特性的 workflow
- **静默性**: 🟡可察觉 — job 层面可见失败但延续，workflow 整体状态与预期不符
- **影响面**: 🟡同维度 — 影响所有使用 continue-on-error 的 workflow
- **综合**: platform 在 workflow 整体状态评估时未正确处理 continue-on-error，导致 job_a 失败时 workflow 被标记为 failure
- **是否有规避手段**: 否（是 platform 层面的状态判定逻辑问题）

**建议**:
- 平台方检查 workflow 状态判定逻辑：当 job 设置了 continue-on-error=true 时，job 失败不应导致 workflow 整体失败
- 对照 GitHub Actions 行为：continue-on-error 的 job 失败不影响后续 job 执行，且 workflow conclusion 取决于最终 job 状态
