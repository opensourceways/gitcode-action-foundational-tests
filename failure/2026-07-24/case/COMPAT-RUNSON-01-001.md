## 失败分诊 · COMPAT-RUNSON-01-001 · runs-on 标签体系——三段式数组正常匹配

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 7 行）:
```
=== JOB: Verify three-part runs-on array (status=COMPLETED) ===
[2026/07/23 22:23:59.912 GMT+08:00] [INFO] Job(1529977405961936896_1529977405928382471) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0e2eff48-33b4-4714-afd2-7d43714c9b48.sh
RUNSON_ARRAY_OK
Runner labels: dedicate-hosted x64 large
```

  **日志分析**: "RUNSON_ARRAY_OK" — runs-on 三段式正常

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNSON-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中声明 `runs-on: [dedicate-hosted, x64, large]`"
  - 操作步骤 2: "触发工作流，观察 Runner 调度行为"
  - 操作步骤 3: "确认 job 被分配到满足所有标签的 Runner 上执行"

  预期结果:
  - 三段式数组格式被平台正确解析
  - job 成功调度到同时满足三个标签的 Runner
  - 工作流正常执行，无标签匹配错误

  验证点:
  - [正向] 工作流成功启动并执行
  - [正向] 日志中显示 Runner 标签与声明一致
  - [负向] 不应因数组格式而被平台拒绝解析

- **实际行为**:
  - "RUNSON_ARRAY_OK" — runs-on 三段式正常


- **测试 YAML 与规格精确对照**:
  - 规格文件: `runner-and-environment.md` (路径: `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md`)
  - 规格节选:
```yaml
# runs-on: [os, arch, size] 三段式标签
# 如 runs-on: [ubuntu-latest, x64, small]
```
    该规格明确声明: runner 标签三段式格式

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"RUNSON_ARRAY_OK" — runs-on 三段式正常）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 runs-on 三段式数组格式正常（RUNSON_ARRAY_OK, Runner labels: dedicate-hosted x64 large），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常调度并输出 Runner 标签，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 runs-on 三段式标签调度功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-RUNSON-01-001 标记为「用例断言修复后应重新验跑」
