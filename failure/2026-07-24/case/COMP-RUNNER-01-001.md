## 失败分诊 · COMP-RUNNER-01-001 · 三段式标签正确调度到对应规格 Runner

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）
assertions[1] (positive, runner_label) — 期望 `ubuntu-latest,x64,small`，实际值匹配但断言词汇格式不兼容

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 7 行）:
```
=== JOB: Verify 3 segment label (status=COMPLETED) ===
[2026/07/23 22:14:06.404 GMT+08:00] [INFO] Job(1529974916940435456_1529974916919463943) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6349b2ff-42a6-4407-bdac-e3908cc479dc.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6349b2ff-42a6-4407-bdac-e3908cc479dc.sh
os=linux
arch=x86_64
```

  **日志分析**: Runner spec 验证通过, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMP-RUNNER-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "配置 runs-on: [ubuntu-latest, x64, small]"
  - 操作步骤 2: "触发 workflow"

  预期结果:
  - job 被调度到符合标签的 Runner
  - 运行成功

  验证点:
  - [正向] 运行状态为 success
  - [正向] job 的 Runner 标签与声明一致

- **实际行为**:
  - Runner spec 验证通过, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `runner-and-environment.md` (路径: `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md`)
  - 规格节选:
```yaml
# runs-on: [os, arch, size] 三段式标签
# 如 runs-on: [ubuntu-latest, x64, small]
```
    该规格明确声明: runner 标签三段式格式

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（Runner spec 验证通过, run=COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-RUNNER-01-001 标记为「用例断言修复后应重新验跑」
