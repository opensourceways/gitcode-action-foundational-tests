## 失败分诊 · USE-DISP-01-002 · workflow_dispatch 未提供参数但存在 default 时应使用默认值运行

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_logs) — 期望日志含 `"env=staging"`，实际 Job FAILED 且无任何步骤输出（0 字节有效日志），run_logs 中不包含该字符串

**根因初判**: 需人工判断
**责任人**: 多方联合

**证据**:

- **Job 日志全量**（2 行）:
  ```
  === JOB: default input value (status=FAILED) ===
  [2026/07/23 22:42:44.561 GMT+08:00] [INFO] Job(1529982123488710656_1529982123467739143) duration check: true
  ```
  Job 状态为 FAILED，日志仅包含 header 和 duration check 行，无任何 shell 脚本创建/执行记录，无步骤输出。无法从日志中判断 `inputs.environment` 的 default 值是否被注入、workflow 是否因表达式问题或调度失败而中断。

- **预期行为**（Phase 01 文本用例 `USE-DISP-01-002`，优先级 P1，维度 usability/completeness）:
  - 操作步骤 1: "手动触发 workflow 不提供该参数"
  - 预期结果: "workflow 使用默认值成功运行"
  - 验证点: "[正向] 运行成功完成"；"[正向] 日志中输出 default 值"

- **实际行为**:
  - Job 在进入步骤执行前即 FAILED，未产生任何步骤日志输出。无法判定失败原因为：(a) `workflow_dispatch` 未注入 default 值导致 `${{ inputs.environment }}` 求值错误；(b) 平台调度器在参数注入阶段失败；(c) 其他环境/Runner 问题。由于 0 字节有效日志，default 值机制是否工作无法确认。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `test-default` job 的 workflow 定义:
    ```yaml
    on:
      workflow_dispatch:
        inputs:
          environment:
            description: target environment
            type: string
            required: false
            default: staging
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/running-pipelines/manually-trigger-pipeline.md` 第 13-53 行的示例:
    ```yaml
    on:
      workflow_dispatch:
        inputs:
          environment:
            description: '部署目标环境'
            required: true
            default: 'staging'
            type: string
    ```
    其中第 22 行 `default: 'staging'` 和第 56 行说明 `inputs` 字段受支持，文档承诺了 default 值机制应正常工作。测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 低（0 字节有效日志，无法从日志中定位具体失败原因；需通过平台后端日志或 UI 进一步排查 default 值注入是否发生）

**影响**:
- **阻塞性**: 🔴阻塞 — Job 在步骤执行前即 FAILED 且无任何步骤输出，workflow 未能完成任何有效工作
- **静默性**: 🟡可察觉 — Job 状态为 FAILED 且 0 字节有效日志，用户明显感知到失败，但失败原因完全不可见
- **影响面**: 🟢单用例 — 仅该特定 workflow_dispatch default 值注入场景受影响，需人工排查具体原因
- **综合**: Job 在步骤执行前即失败且无有效日志，阻塞执行但具体原因需人工排查平台后端
- **是否有规避手段**: 否 — 当前无有效诊断信息可供用户自行排查

**建议**:
- 需在平台侧排查该 Job 失败的具体原因（Runner 调度日志、表达式求值日志），确认 `workflow_dispatch` + `default` 值在不传参场景下是否正常运行
- 若确认为平台缺陷：修复 `inputs` default 值注入逻辑
- 若确认为用例/环境问题：在测试 YAML 中添加更强的故障信号输出
- 相关用例: USE-DISP-01-001（同一维度 sibling）
