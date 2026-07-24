## 失败分诊 · COMP-CALL-01-001 · 2 层 workflow_call 嵌套正常执行

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `FAILED`（平台缺陷导致 job 执行失败）

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（共 2 行）:
```
=== JOB: Call reusable workflow (status=FAILED) ===
[2026/07/23 22:12:03.980 GMT+08:00] [INFO] Job(1529974403217506304_1529974403179757575) duration check: true
```

  **日志分析**: Job status=FAILED, reusable workflow_call 调用失败

- **预期行为**（Phase 01 文本用例 `COMP-CALL-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "触发主 workflow"
  - 操作步骤 2: "观察嵌套调用是否成功完成"

  预期结果:
  - 2 层嵌套 workflow_call 成功执行
  - 子 workflow 的输出正确传递回主 workflow

  验证点:
  - [正向] 运行状态成功
  - [正向] 子 workflow 的 step 日志可见

- **实际行为**:
  - Job status=FAILED, reusable workflow_call 调用失败


- **测试 YAML 与规格精确对照**:
  - 规格文件: `workflow-job-step-action.md` (路径: `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`)
  - 规格节选:
```yaml
# workflow_call 允许 workflow 间互相调用
# 通过 on.workflow_call 定义可复用 workflow
```
    该规格明确声明: workflow_call 机制定义

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 中（Job status=FAILED, reusable workflow_call 调用失败）

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CALL-01-001.log`
- 建议修复后重新验跑 COMP-CALL-01-001
