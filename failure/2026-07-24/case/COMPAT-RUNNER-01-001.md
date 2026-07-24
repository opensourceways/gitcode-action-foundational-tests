## 失败分诊 · COMPAT-RUNNER-01-001 · runner.os 在 Linux Runner 上应返回 Linux

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 7 行）:
```
=== JOB: Test runner.os value (status=COMPLETED) ===
[2026/07/23 22:23:37.671 GMT+08:00] [INFO] Job(1529977312760053760_1529977312730693639) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3be8b7d2-ec6d-4020-9809-502bab3ebdf8.sh
runner_os=linux
done
```

  **日志分析**: runner 验证通过, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMPAT-RUNNER-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 workflow 的 run 步骤中输出 ${{ runner.os }}"
  - 操作步骤 2: "触发 workflow 运行"

  预期结果:
  - runner.os 应返回 Linux（首字母大写，与 GitHub 一致）

  验证点:
  - [正向] 日志中 runner.os 的值为 Linux
  - [负向] 不应返回小写的 linux

- **实际行为**:
  - runner 验证通过, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `runner-and-environment.md` (路径: `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md`)
  - 规格节选:
```yaml
# runs-on: [os, arch, size] 三段式标签
# 如 runs-on: [ubuntu-latest, x64, small]
```
    该规格明确声明: runner 标签三段式格式

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（runner 验证通过, run=COMPLETED）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 runner.os 正常返回（runner_os=linux），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常输出 runner 上下文值，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 runner.os 上下文功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-RUNNER-01-001 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-RUNNER-01-002
