## 失败分诊 · COMP-PUSH-01-001 · 匹配 branches 的 push 正确触发 workflow

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）
assertions[1] (positive, run_event) — 期望 `push`，实际值匹配但断言词汇格式不兼容

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Verify branch trigger (status=COMPLETED) ===
[2026/07/23 22:13:15.010 GMT+08:00] [INFO] Job(1529974701441290240_1529974701416124423) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/04c682c0-7a35-4080-9caa-44265ee2138f.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/04c682c0-7a35-4080-9caa-44265ee2138f.sh
triggered on main
```

  **日志分析**: "triggered on main" — push 触发成功, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMP-PUSH-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "向 main 分支推送代码"
  - 操作步骤 2: "观察 workflow 是否触发"

  预期结果:
  - push 到 main 分支触发 workflow 运行

  验证点:
  - [正向] 运行记录存在且 event 为 push
  - [正向] head_branch 为 main

- **实际行为**:
  - "triggered on main" — push 触发成功, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `trigger-events.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/trigger-events.md`)
  - 规格节选:
```yaml
on:
  push:
    branches:
      - main
```
    该规格明确声明: push 事件触发定义

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"triggered on main" — push 触发成功, run=COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-PUSH-01-001 标记为「用例断言修复后应重新验跑」
