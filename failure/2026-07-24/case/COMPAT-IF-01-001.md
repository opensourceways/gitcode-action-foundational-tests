## 失败分诊 · COMPAT-IF-01-001 · step 失败后后续 step 默认跳过行为

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `failure`，实际 `FAILED`（平台 API 大小写与表达式函数语义不一致：platform=`FAILED` vs `${{ failure }}`=`failed`）

**根因初判**: Engine Bug

**证据**:

- **Job 日志全量**（共 6 行）:
```
=== JOB: Test step failure skip (status=FAILED) ===
[2026/07/23 22:21:08.975 GMT+08:00] [INFO] Job(1529976689461440512_1529976689440468999) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/f8929145-2912-4162-b2f8-5b8787004f1b.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/f8929145-2912-4162-b2f8-5b8787004f1b.sh
::error::Process exited with code 1
```

  **日志分析**: 故意失败 job → "failure"≠"FAILED", leak=PASS

- **预期行为**（Phase 01 文本用例 `COMPAT-IF-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "提交一个包含两个 step 的 workflow"
  - 操作步骤 2: "第一个 step 显式返回非零退出码以模拟失败"
  - 操作步骤 3: "第二个 step 输出一条消息"
  - 操作步骤 4: "手动触发该 workflow"

  预期结果:
  - 第一个 step 失败后，第二个 step 被系统默认跳过
  - 整个 job 标记为失败状态

  验证点:
  - [正向] 第二个 step 未执行，日志中无其输出
  - [正向] job 整体状态为失败
  - [负向] 第二个 step 不应在第一个 step 失败后仍运行

- **实际行为**:
  - 故意失败 job → "failure"≠"FAILED", leak=PASS


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

**置信度**: 高（故意失败 job → "failure"≠"FAILED", leak=PASS）

**影响**:
- **阻塞性**: ⚪无影响 — Engine Bug（大小写比较），平台 step 失败后默认跳过正常，仅断言 "failure"≠"FAILED"
- **静默性**: 🟢明确报错 — 平台输出 "::error::Process exited with code 1"，错误清晰可诊断
- **影响面**: 🟢单用例 — 表达式引擎大小写不一致，仅影响断言比较
- **综合**: 平台 step 失败跳过行为正确，仅表达式返回值大小写与断言不匹配
- **是否有规避手段**: 是 — 统一断言为 FAILED 或平台修复大小写语义

**建议**:
- 平台表达式引擎同时返回大写(`FAILED`/`CANCELED`)和文档中的小写(`success`/`failure`/`cancelled`)值
- 建议统一为文档约定的小写语义值
- 将 COMPAT-IF-01-001 标记为「平台修复后重新验跑」
- 相关用例: COMPAT-IF-01-002
