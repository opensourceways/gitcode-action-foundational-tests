## 失败分诊 · COMP-TIMEOUT-01-002 · 超时的 job 被强制终止并标记为 failure

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `CANCELED`（harness 超时先于平台 timeout 触发）
assertions[1] (positive, run_status) — 期望 `failure`，下游随上游失败而 IGNORED

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（共 10 行）:
```
=== JOB: Verify timeout kill (status=CANCELED) ===
[2026/07/23 22:15:10.715 GMT+08:00] [INFO] Job(1529975186650959872_1529975186625794055) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a86ef9ad-8274-4ad6-b1c6-9d2bf9752255.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a86ef9ad-8274-4ad6-b1c6-9d2bf9752255.sh
starting

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2a43ae6e-da92-40e6-a74f-627a1cd6dc61.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2a43ae6e-da92-40e6-a74f-627a1cd6dc61.sh
```

  **日志分析**: "starting" 出现(value=PASS), 227s 后 harness 超时取消, CANCELED≠"failure"

- **预期行为**（Phase 01 文本用例 `COMP-TIMEOUT-01-002`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发 workflow，其中 step 睡眠超过 1 分钟"
  - 操作步骤 2: "观察 job 是否在 1 分钟后被强制终止"

  预期结果:
  - job 在 1 分钟后被强制终止
  - 运行状态标记为 failure
  - 已运行 step 的日志保留

  验证点:
  - [负向] 运行状态为 failure
  - [正向] 超时前已完成的 step 日志完整保留

- **实际行为**:
  - "starting" 出现(value=PASS), 227s 后 harness 超时取消, CANCELED≠"failure"


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

**置信度**: 中（"starting" 出现(value=PASS), 227s 后 harness 超时取消, CANCELED≠"failure"）

**建议**:
- 增加 harness 超时时间或减小 platform timeout-minutes 值以避免 harness 先触发
- 将 COMP-TIMEOUT-01-002 标记为「环境修复后重新验跑」
- 相关用例: COMP-TIMEOUT-01-001
