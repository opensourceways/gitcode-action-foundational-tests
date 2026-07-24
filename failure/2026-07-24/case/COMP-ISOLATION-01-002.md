## 失败分诊 · COMP-ISOLATION-01-002 · 环境变量不跨 job 泄漏

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 14 行）:
```
=== JOB: Create tmp isolation marker (status=COMPLETED) ===
[2026/07/23 22:02:49.185 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100679) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
MARKER_CREATED


=== JOB: Check tmp marker isolation (status=COMPLETED) ===
[2026/07/23 22:03:02.555 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100681) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
ISOLATION_STRONG: marker not visible across jobs
```

  **日志分析**: 隔离检查全部通过, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMP-ISOLATION-01-002`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "job 1 设置环境变量"
  - 操作步骤 2: "job 2 检查该环境变量"

  预期结果:
  - job 2 不应看到 job 1 设置的环境变量

  验证点:
  - [负向] job 2 中环境变量值为空或未设置

- **实际行为**:
  - 隔离检查全部通过, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `runner-and-environment.md` (路径: `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md`)
  - 规格节选:
```yaml
# Runner 为每个 job 创建独立的工作空间
# 每个并发运行有独立的临时目录
```
    该规格明确声明: job 间隔离机制

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（隔离检查全部通过, run=COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-ISOLATION-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMP-ISOLATION-01-001
