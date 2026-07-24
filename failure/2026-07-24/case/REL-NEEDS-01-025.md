## 失败分诊 · REL-NEEDS-01-025 · needs 失败传播——上游 job 失败时下游 job 应被 skip

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望下游 job_b 状态=skipped，实际 job_b status=IGNORED；assertions[1] (positive, run_logs) — 期望日志含 "skipped"，实际不存在

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 9 行）:
  ```
  === JOB: upstream failing job (status=FAILED) ===
  [2026/07/23 22:33:52.461 GMT+08:00] [INFO] Job(1529979891682521088_1529979891657355271) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c1c13e84-9d75-4ff3-b3ad-c9e88d6a8a55.sh
  ::error::Process exited with code 1

  === JOB: downstream dependent job (status=IGNORED) ===
  ```
  日志显示：**平台行为完全正确**——upstream job 执行 `exit 1` 失败（`Process exited with code 1`），下游 job 因 `needs` 依赖被忽略（**status=IGNORED**）。但断言期望的状态值是 **`skipped`**，而非平台实际使用的 **`IGNORED`**。这是**词汇差异**——平台使用 `IGNORED` 标记因上游失败而被跳过不执行的下游 job，而断言期望 `skipped`。

- **预期行为**（Phase 01 文本用例 `REL-NEEDS-01-025`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 job_a(失败) 和 job_b(needs: job_a) 的 workflow"
  - 预期结果: "job_a 状态=failure；job_b 状态=skipped；job_b 不应执行"
  - 验证点: "[正向] job_a 状态=failure；[正向] job_b 状态=skipped；[负向] job_b 不应在 job_a 失败后仍执行"

- **实际行为**:
  - job_a FAILED（exit 1）——符合预期
  - job_b IGNORED（未执行）——符合预期（平台正确拒绝执行）
  - 平台行为完全正确，但断言期望 `skipped` 而平台使用 `IGNORED`

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `downstream dependent job` 配置 `needs: upstream failing job`，上游 job 执行 `exit 1`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/configure-conditional-execution.md` 中 `needs` 的失败传播行为定义。规格描述：当 `needs` 依赖的上游 job 失败时，下游 job 会被跳过不执行。平台使用 `IGNORED` 状态标记此种情况——这与规范 `skipped` 的语义等价，但词汇不同。**平台功能正确，断言词汇不匹配**。

**置信度**: 高（平台行为完全正确——上游 FAILED → 下游 IGNORED，符合 needs 失败传播语义；失败纯因状态词汇差异：`IGNORED` vs 预期的 `skipped`）

**建议**:
- 修正断言中的状态标记——将 `skipped` 改为 `IGNORED`（匹配平台实际状态值体系）
- 相关用例: REL-CONTINUE-01-030
