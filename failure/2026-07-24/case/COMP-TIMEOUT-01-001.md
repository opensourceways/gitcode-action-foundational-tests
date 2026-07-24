## 失败分诊 · COMP-TIMEOUT-01-001 · 未声明 timeout-minutes 的 job 在 360 分钟内正常完成

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Verify default timeout (status=COMPLETED) ===
[2026/07/23 22:14:59.297 GMT+08:00] [INFO] Job(1529975138676383744_1529975138642829319) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0850d2a0-1db9-47e0-a3df-bc88b583695b.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0850d2a0-1db9-47e0-a3df-bc88b583695b.sh
done
```

  **日志分析**: "done" — 在 73s 内完成(<360min), 断言期望 "starting" > "done" 但 run_status 词汇不匹配

- **预期行为**（Phase 01 文本用例 `COMP-TIMEOUT-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发 workflow"
  - 操作步骤 2: "观察运行是否成功"

  预期结果:
  - job 在默认 360 分钟超时范围内成功完成

  验证点:
  - [正向] 运行状态为 success
  - [非功能] 运行耗时远小于 360 分钟

- **实际行为**:
  - "done" — 在 73s 内完成(<360min), 断言期望 "starting" > "done" 但 run_status 词汇不匹配


- **测试 YAML 与规格精确对照**:
  - 规格文件: `configure-jobs.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/configure-jobs.md`)
  - 规格节选:
```yaml
jobs:
  test:
    timeout-minutes: 360
```
    该规格明确声明: timeout-minutes 配置字段

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"done" — 在 73s 内完成(<360min), 断言期望 "starting" > "done" 但 run_status 词汇不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台默认超时正常（73s 内完成远小于 360min，输出 "done"），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常完成 job，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台默认 timeout-minutes 功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-TIMEOUT-01-001 标记为「用例断言修复后应重新验跑」
- 相关用例: COMP-TIMEOUT-01-002
