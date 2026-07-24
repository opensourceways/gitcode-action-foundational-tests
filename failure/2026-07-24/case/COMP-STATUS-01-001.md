## 失败分诊 · COMP-STATUS-01-001 · 运行状态机 queued 到 completed 转换正确

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status_sequence) — 期望 `queued_in_progress_completed`，实际值与期望不匹配（词汇映射缺失）
assertions[1] (positive, run_status) — 期望 `success`，实际值匹配但断言词汇格式不兼容

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Verify status transitions (status=COMPLETED) ===
[2026/07/23 22:14:18.376 GMT+08:00] [INFO] Job(1529974967082958848_1529974967053598727) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/12939bab-f456-413b-8825-3a3e589aec8b.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/12939bab-f456-413b-8825-3a3e589aec8b.sh
running
```

  **日志分析**: "running" — run=COMPLETED, 断言词汇不匹配

- **预期行为**（Phase 01 文本用例 `COMP-STATUS-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发 workflow"
  - 操作步骤 2: "轮询 API 观察状态转换"

  预期结果:
  - 状态依次为 queued -> in_progress -> completed(success)

  验证点:
  - [正向] 状态转换序列符合预期
  - [正向] 最终状态为 completed/success

- **实际行为**:
  - "running" — run=COMPLETED, 断言词汇不匹配


- **测试 YAML 与规格精确对照**:
  - 规格文件: `view-run-results.md` (路径: `phase01/inputs/gitcode-spec/running-pipelines/view-run-results.md`)
  - 规格节选:
运行状态枚举: COMPLETED / FAILED / CANCELED / IGNORED
    该规格明确声明: 运行状态语义

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"running" — run=COMPLETED, 断言词汇不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台状态机正常工作（"running" 输出确认 job 正常执行），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常完成 job 并输出运行状态，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台运行状态机功能正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-STATUS-01-001 标记为「用例断言修复后应重新验跑」
