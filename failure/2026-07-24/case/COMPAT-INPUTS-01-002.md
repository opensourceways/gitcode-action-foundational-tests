## 失败分诊 · COMPAT-INPUTS-01-002 · workflow_dispatch inputs 类型限制 - string 正常通过

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 7 行）:
```
=== JOB: Verify string input acceptance (status=COMPLETED) ===
[2026/07/23 22:21:44.341 GMT+08:00] [INFO] Job(1529976837469913088_1529976837436358663) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/20a4cb42-6949-4714-bb01-d9812980ffa0.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/20a4cb42-6949-4714-bb01-d9812980ffa0.sh
ENV=production
STRING_INPUT_OK
```

  **日志分析**: "STRING_INPUT_OK", "ENV=production" — inputs 传递正常

- **预期行为**（Phase 01 文本用例 `COMPAT-INPUTS-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 workflow 中定义 workflow_dispatch inputs 并指定 type: string"
  - 操作步骤 2: "提交并推送该 workflow"
  - 操作步骤 3: "触发 workflow 并传入参数"

  预期结果:
  - workflow 应被平台接受，不报错
  - string 类型的 input 应能正常接收和输出

  验证点:
  - [正向] workflow 校验通过
  - [正向] string 类型 input 能正常传递和使用

- **实际行为**:
  - "STRING_INPUT_OK", "ENV=production" — inputs 传递正常


- **测试 YAML 与规格精确对照**:
  - 规格文件: `context.md / expressions.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/context.md`)
  - 规格节选:
```yaml
# context.md 第29-31行: atomgit.ref 为完整引用名
# 如 refs/heads/main
# expressions.md 第36-39行: success/failed 状态函数定义
```
    该规格明确声明: context.md 27-33行 atomgit 上下文属性 + expressions.md 36-39行状态函数

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"STRING_INPUT_OK", "ENV=production" — inputs 传递正常）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 inputs string 类型传递正常（STRING_INPUT_OK, ENV=production），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常传递并输出 input 值，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 workflow_dispatch inputs 功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-INPUTS-01-002 标记为「用例断言修复后应重新验跑」
