## 失败分诊 · COMPAT-IF-01-002 · continue-on-error 标记后失败 step 不阻断后续执行

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 11 行）:
```
=== JOB: Test continue on error (status=COMPLETED) ===
[2026/07/23 22:21:22.562 GMT+08:00] [INFO] Job(1529976746424537088_1529976746403565575) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
This should appear
```

  **日志分析**: "This should appear" — if true step 正常执行

- **预期行为**（Phase 01 文本用例 `COMPAT-IF-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "提交一个包含两个 step 的 workflow"
  - 操作步骤 2: "第一个 step 显式返回非零退出码，但设置 continue-on-error 为 true"
  - 操作步骤 3: "第二个 step 输出一条消息"
  - 操作步骤 4: "手动触发该 workflow"

  预期结果:
  - 第一个 step 虽失败，但因 continue-on-error 标记，后续 step 仍继续执行
  - job 整体状态可能为成功或特殊标记，但不因该失败而中断

  验证点:
  - [正向] 第二个 step 成功执行并输出消息
  - [正向] 第一个 step 的失败后，后续 step 未被跳过
  - [正向] job 未在第一个 step 处中断

- **实际行为**:
  - "This should appear" — if true step 正常执行


- **测试 YAML 与规格精确对照**:
  - 规格文件: `expressions.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/expressions.md`)
  - 规格节选:
```yaml
# expressions.md 第36-39行: success/failed 状态函数
# context.md 第202-207行: steps 上下文 outcome 与 conclusion
steps:<step_id>.conclusion 的值: success / failure / cancelled
```
    该规格明确声明: expressions.md 36-39行 + context.md 202-207行

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"This should appear" — if true step 正常执行）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-IF-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-IF-01-001
