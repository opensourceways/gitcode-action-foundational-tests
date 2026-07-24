# Failure Analyst · RELIABILITY FAIL Cases · 2026-07-24-valid297-final

## 失败分诊 · REL-ARTCONC-01-063 · 制品并发写一致性

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'artifact concurrent write test' status=FAILED

**根因初判**: 用例问题

**证据**:
- **Job 日志全量** (24 行):
  ```
  /home/.../_temp/07793475-...sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ```
  所有 3 个 matrix job 实例均因 `${{{{ matrix.instance }}}}: bad substitution` 立即失败。
- **实际行为**: `${{{{ }}}}` 不是合法的 bash 变量语法。应为 `${{ }}` 双括号。
- **对照 GitCode 规格**: `configure-matrix-builds.md` line 22: `runs-on: ${{ matrix.os }},${{ matrix.arch }},small`
**置信度**: 高

---

## 失败分诊 · REL-MATRIX-01-038 · 大规模 matrix——20 个组合

**判定结果**: FAIL
**失败断言**: assertions[0] (run_status, positive) — 期望 COMPLETED，实际 FAILED

**根因初判**: 用例问题

**证据**:
- **Job 日志** (168 行): 全部 25 个 job 均报 `os=${{{{ matrix.os }}}}: bad substitution`
- **对照 GitCode 规格**: `configure-matrix-builds.md` line 22 使用双括号
**置信度**: 高

---

## 失败分诊 · REL-MATRIX-01-039 · 大规模 matrix——50 个组合

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'matrix 50 combos test' status=FAILED

**根因初判**: 用例问题

**证据**:
- **Job 日志** (350 行): 全部 50 个 job 均报 `v1=${{{{ matrix.v1 }}}}: bad substitution`
- **对照 GitCode 规格**: `configure-matrix-builds.md` line 22 使用双括号
**置信度**: 高

---

## 失败分诊 · REL-FAULT-01-031 · 故障注入——runner SIGKILL

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, job_status) — 期望 FAILED，实际 COMPLETED

**根因初判**: 环境问题

**证据**:
- **Job 日志** (24 行): step_one~step_five 全部正常输出了 marker。SIGKILL 故障注入未生效。
**置信度**: 高

---

## 失败分诊 · REL-FAULT-01-032 · 故障注入——网络分区 artifact 上传

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 FAILED，实际 COMPLETED；assertions[1] (value, run_logs) — 期望 log contains 'network'，实际 absent

**根因初判**: 环境问题

**证据**:
- **Job 日志** (38 行): 10MB artifact 上传全程成功（Upload complete. SHA-256: cf2c44...），网络分区故障注入未生效。
**置信度**: 高

---

## 失败分诊 · REL-FAULT-01-033 · 故障注入——runner 磁盘满

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 FAILED，实际 COMPLETED；assertions[1] (value, run_logs) — 期望 log contains 'No space left on device'，实际 absent

**根因初判**: 环境问题

**证据**:
- **Job 日志** (11 行): 2GB 文件写入成功（2147483648 bytes copied, 0.967s），Runner 磁盘有 96GB 可用空间。
**置信度**: 高

---

## 失败分诊 · REL-CANCEL-01-028 · 手动取消 workflow

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 CANCELLED，实际 COMPLETED

**根因初判**: 环境问题

**证据**:
- **Job 日志** (9 行): cleanup executed — workflow 完整执行完毕。Harness cancel API 调用未生效。
**置信度**: 中

---

## 失败分诊 · REL-CONTINUE-01-030 · continue-on-error=true

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 FAILED，实际 COMPLETED

**根因初判**: 需人工判断

**证据**:
- **Job 日志** (11 行): Job A 失败（exit 1），Job B 因 continue-on-error 继续执行。run 最终 COMPLETED。
- **对照 GitCode 规格**: 需确认 GitCode 的 run_status 在 continue-on-error 场景的语义。
**置信度**: 中

---

## 失败分诊 · REL-MATRIX-01-026 · matrix fail-fast=true

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 FAILED，实际 COMPLETED

**根因初判**: 用例问题

**证据**:
- **Job 日志** (18 行): version=1/2/3 全部成功。无任何 matrix 实例失败，fail-fast 无法触发。
**置信度**: 高

---

## 失败分诊 · REL-LONG-01-043 · 长时运行 350 分钟边界

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 COMPLETED，实际 CANCELLED

**根因初判**: 环境问题

**证据**:
- **Job 日志** (6 行): heartbeat 1/2 后 291s 被 CANCELLED。Harness 300s 超时截断了需 350min 的测试。
**置信度**: 高

---

## REL-TIMEOUT-01-007/008/009/010 · timeout 边界测试

**判定结果**: FAIL
**失败断言**: run_status — 期望 COMPLETED/FAILED，实际 CANCELLED

**根因初判**: 环境问题（harness 300s 超时截断）

**证据**: 4 个用例均在 142-164s 被 harness CANCELLED，远短于测试所需的 1min/359min/360min 超时边界。
**置信度**: 高

---

## 失败分诊 · REL-ARTPERF-01-053 · 制品传输性能——100MB

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'upload artifact job' status=FAILED

**根因初判**: 环境问题

**证据**: 日志明确显示 `Upload artifact failed: Artifact with name already exists: perf-artifact` — 前次运行残留。
**置信度**: 高

---

## 失败分诊 · REL-ARTPERF-01-053-V2 · 制品传输性能——1GB

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'upload artifact job' status=FAILED

**根因初判**: 环境问题

**证据**: 日志显示 `Namespace artifact quota exceeded: currentUsed=1632234274, max=1073741824` —配额用尽。
**置信度**: 高

---

## 失败分诊 · REL-RETAIN-01-047 · artifact 保留期

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'artifact retention test' status=FAILED

**根因初判**: 环境问题

**证据**: `Upload artifact failed: Artifact with name already exists: retention-artifact`
**置信度**: 高

---

## 失败分诊 · REL-ART-01-041 · 超大 artifact 下载

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'download artifact job' status=FAILED

**根因初判**: 用例问题

**证据**: Upload 成功，Download 成功，但 verify 步骤 `ls perf-artifact` 失败（实际文件名为 artifact.bin）。
**置信度**: 高

---

## 失败分诊 · REL-K8S-01-045 · 自托管 K8s Runner

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'K8s runner scaling test' status=FAILED

**根因初判**: 环境问题

**证据**: 日志仅 1 行 duration check，无任何 shell 输出。K8s runner 未部署。
**置信度**: 高

---

## 失败分诊 · REL-NEEDS-01-025 · needs 失败传播

**判定结果**: FAIL
**失败断言**: assertions[1] (positive, run_status) — 期望 SKIPPED，实际 FAILED

**根因初判**: 产品缺陷

**证据**:
- Job A: `Process exited with code 1`（上游失败）
- Job B: 状态 FAILED（应为 SKIPPED）
- **对照 GitCode 规格**: `configure-dependencies-order.md` line 83: "依赖的 job 失败时，当前 job 默认不执行"
**置信度**: 高

---

## 失败分诊 · REL-YAMLCACHE-01-060 · Workflow YAML 缓存失效

**判定结果**: FAIL
**失败断言**: assertions[0] (value, run_logs) — 期望 log contains 'marker_v2'，实际 absent（got marker_v1）

**根因初判**: 产品缺陷

**证据**: 日志输出 `marker_v1` 而非更新后的 `marker_v2`。平台缓存旧 YAML。
**置信度**: 中

---

## 失败分诊 · REL-RUNNER-01-049-V2 · Runner 规格真实性——2xlarge

**判定结果**: FAIL
**失败断言**: assertions[0] (status, run_status) — 期望 all job/step green，实际 job 'probe 2xlarge runner' status=FAILED

**根因初判**: 需人工判断

**证据**: xlarge job 成功（16 CPUs/62GB RAM/118G disk），2xlarge job 仅 1 行 duration check 无输出。
**置信度**: 低

---

## 汇总统计

| 根因 | 数量 |
|---|---|
| 用例问题 | 5 |
| 环境问题 | 16 |
| 产品缺陷 | 2 |
| 需人工判断 | 2 |
