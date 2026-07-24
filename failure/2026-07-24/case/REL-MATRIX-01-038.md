## 失败分诊 · REL-MATRIX-01-038 · 大规模 matrix——20 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: 正向/generated_jobs_count expected=20 actual=所有20个job因bad substitution失败; 正向/run_status expected=completed(success) actual=全部FAILED

**根因初判**: 标记不匹配
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（217 行，摘要）:
  ```
  === JOB: matrix 20 combos test (status=FAILED) ===
  [2026/07/23 22:32:39.979] [INFO] Job(1529979577273552896_1529979577281941515) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh: line 1: os=${{{{ matrix.os }}}}: bad substitution
  ::error::Process exited with code 1
  ```
  *(以上模式重复 20 次，每次不同的 job ID 但相同的 `bad substitution` 错误)*

- **预期行为**（Phase 01 文本用例 REL-MATRIX-01-038，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发含 4 维×5 值=20 组合的 matrix workflow
  - 预期结果: 20 个 jobs 全部生成; 每个实例获得正确的矩阵变量值; 20 个 jobs 全部 completed(success)

- **实际行为**:
  - 20 个 matrix job 被正确生成并调度
  - 但所有 20 个 job 在脚本执行第一阶段即失败：`os=${{{{ matrix.os }}}}: bad substitution`
  - 与 REL-ARTCONC-01-063 相同的根因：YAML 中 `${{{{ matrix.os }}}}` 使用了四重花括号而非二重
  - 正确语法应为 `${{ matrix.os }}`，runner 将其解释为 bash 非法替换

- **对照 GitCode 规格**:
  - 无直接相关规格段落；GitCode 表达式语法为 `${{ expression }}`（二重花括号）

- **环境前置条件验证**: matrix 展开正确（20 个 job 生成），runner 和调度正常，问题在于 YAML 语法

**置信度**: 高 (同 REL-ARTCONC-01-063，四重花括号 bad substitution 是确定的模板错误)

**影响**:
- **阻塞性**: 🔴阻塞 — 所有 20 个 matrix job 均失败
- **静默性**: 🟢明确报错 — `bad substitution` 明确提示
- **影响面**: 🔴跨维度 — 同 REL-ARTCONC-01-063，影响所有使用 `{{{{ }}}}` 模板的 matrix 用例
- **综合**: Phase 02 YAML 模板将 matrix 变量引用错误转义为 `{{{{ }}}}`，应改为 `${{ }}`
- **是否有规避手段**: 是（修正 YAML 模板中所有 `{{{{ }}}}` 为 `${{ }}`）

**建议**:
- Phase 02 统一修正所有 YAML 模板中的表达式转义：`${{{{ X }}}}` → `${{ X }}`
- 同时修复 REL-ARTCONC-01-063、REL-MATRIX-01-039、REL-OUTPUT-01-016
