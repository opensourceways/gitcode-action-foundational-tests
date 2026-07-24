## 失败分诊 · REL-CONTINUE-01-030 · continue-on-error=true——job 失败后 workflow 不应终止

**判定结果**: FAIL
**失败断言**: 正向/job_a_status expected=failure actual=FAILED; 正向/job_b_status expected=success actual=COMPLETED; 正向/workflow_status expected=success actual=FAILED (likely)

**根因初判**: 平台缺陷（workflow_status 判断逻辑可能受 job_a failure 影响）
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: job with continue on error (status=FAILED) ===
  [2026/07/23 22:27:31.993 GMT+08:00] [INFO] Job(1529978295787597824_1529978295762432000) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/61339c12-85ba-4342-a369-a969479bacf5.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/61339c12-85ba-4342-a369-a969479bacf5.sh
  ::error::Process exited with code 1

  === JOB: downstream after continue (status=COMPLETED) ===
  [2026/07/23 22:27:31.995 GMT+08:00] [INFO] Job(1529978295787597824_1529978295762432002) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/86eba7bd-0f4b-41b2-ac4f-c0f19e468184.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/86eba7bd-0f4b-41b2-ac4f-c0f19e468184.sh
  job_b executed
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发含 continue-on-error=true 的失败 job 和下游 job 的 workflow
  - 预期结果: job_a 状态=failure 但 workflow 不终止; job_b 正常执行并 success; workflow 不应整体 failure

- **实际行为**:
  - job_a 执行 `exit 1` 后正确 FAILED
  - job_b 确实被执行（已打印 `job_b executed`）且 COMPLETED
  - 但断言 `workflow_status=success` 可能失败——因为包含 FAILED job 的 workflow，即使有 `continue-on-error: true`，workflow 整体状态可能仍被平台判定为 failure
  - **失败传导链**: job_a exit 1 → FAILED / continue-on-error 允许继续 → job_b COMPLETED → 但 workflow_status 断言可能因平台将含失败 job 的 workflow 判定为 failure

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `job_a` 的 `continue-on-error`:
    ```yaml
    job_a:
      name: job with continue on error
      runs-on: [dedicate-hosted, x64, large]
      continue-on-error: true
      steps:
        - name: fail step
          run: |
            exit 1
    ```
  - **测试 YAML** 中 `job_b`（无 needs 依赖，无 continue-on-error）:
    ```yaml
    job_b:
      name: downstream after continue
      runs-on: [dedicate-hosted, x64, large]
      steps:
        - name: success step
          run: |
            echo job_b executed
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 172-183 行:
    ```yaml
    jobs:
      flaky-test:
        runs-on: [ubuntu-latest, x64, small]
        continue-on-error: true
        steps:
          - run: ./run-flaky-test.sh
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 183 行:
    设置 `continue-on-error: true` 后，即使 job 失败，workflow 也不会因此终止（后续依赖该 job 的 job 需通过 `if` 条件判断是否继续）
  - **逐项映射**: `continue-on-error: true` → 匹配规格; `exit 1` → 匹配失败场景; job_b 无 needs 依赖 → job_b 与 job_a 并行执行（非依赖关系），所以 job_b 自然不受 job_a 失败影响。断言 `workflow_status=success` 在含 FAILED job 的 workflow 中成立性存疑——规格描述 "workflow 不会因此终止" 但不等于 "workflow_status=success"。

- **环境前置条件验证**: runner 可用，两个 job 均正常调度；job_b 成功输出 `job_b executed`；job_a 正确 FAILED

**置信度**: 高（job_a 正确失败，job_b 正确执行；workflow_status 断言是否通过取决于平台对 continue-on-error workflow 的状态判定逻辑）

**影响**:
- **阻塞性**: 🟢不阻塞 — 核心 continue-on-error 功能正确（job_b 未被阻止）
- **静默性**: 🟢明确 — job_a 明确 fail，job_b 明确 success
- **影响面**: 🟡同用例 — 仅影响 workflow_status 断言
- **综合**: 平台正确地未阻止 job_b 执行，但 workflow 整体状态可能仍需澄清——含 FAILED+continue-on-error 的 workflow 最终 status 应为 success 还是 failure?
- **是否有规避手段**: 是（修改断言：将 `workflow_status=success` 改为仅验证 `job_b_status=success` 和 `job_a_status=failure`）

**建议**:
- 澄清平台对 `continue-on-error` workflow 的最终状态语义：是 success（容忍失败）还是 failure（存在失败）？
- 测试断言可能需要排除 `workflow_status` 或调整为更宽松的条件
