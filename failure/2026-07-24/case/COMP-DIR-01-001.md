## 失败分诊 · COMP-DIR-01-001 · .gitcode/workflows/ 下的 YAML 被正确识别并触发

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）
assertions[1] (positive, run_file_path) — 期望 `.gitcode/workflows/ci.yml`，实际值匹配但断言词汇格式不兼容

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Verify directory recognition (status=COMPLETED) ===
[2026/07/23 22:13:10.568 GMT+08:00] [INFO] Job(1529974682319458304_1529974682290098183) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/195d75a3-e78a-4d88-889d-797372ff1ad1.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/195d75a3-e78a-4d88-889d-797372ff1ad1.sh
workflow recognized
```

  **日志分析**: "workflow recognized" — run=COMPLETED, 断言期望 "success" ≠ 平台 COMPLETED

- **预期行为**（Phase 01 文本用例 `COMP-DIR-01-001`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "向默认分支推送代码变更"
  - 操作步骤 2: "观察 Actions 标签页是否出现新运行"

  预期结果:
  - .gitcode/workflows/ci.yml 被识别为 workflow
  - push 事件触发该 workflow 执行
  - 运行状态最终变为 completed/success

  验证点:
  - [正向] 运行记录存在且 file_path 为 .gitcode/workflows/ci.yml
  - [正向] 运行状态成功完成

- **实际行为**:
  - "workflow recognized" — run=COMPLETED, 断言期望 "success" ≠ 平台 COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `workflow-file-location-structure.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md`)
  - 规格节选:
```yaml
# .gitcode/workflows/<workflow-name>.yml 目录
# 仅 .yml 和 .yaml 后缀的文件会被识别
```
    该规格明确声明: 37-41行明确规定 `.gitcode/workflows/` 为 workflow 文件存放目录

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"workflow recognized" — run=COMPLETED, 断言期望 "success" ≠ 平台 COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMP-DIR-01-001 标记为「用例断言修复后应重新验跑」
