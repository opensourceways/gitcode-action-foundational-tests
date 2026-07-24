## 失败分诊 · REL-MATRIX-01-038 · 大规模 matrix——20 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 20 个 jobs 全部 success，实际所有 job 均 FAILED；assertions[1] (positive, run_logs) — 期望日志含矩阵变量值，实际无任何业务逻辑输出

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 217 行）:
  ```
  === JOB: matrix 20 combos test (status=FAILED) ===
  [2026/07/23 22:32:39.979 GMT+08:00] [INFO] Job(1529979577273552896_1529979577281941515) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh: line 1: os=${{{{ matrix.os }}}}: bad substitution
  ::error::Process exited with code 1

  === JOB: matrix 20 combos test (status=FAILED) ===
  ...（重复 20 次相同的 bad substitution 错误）...
  ```
  日志显示：**20 个 matrix job 实例全部在 bash 第一行报错**——`os=${{{{ matrix.os }}}}: bad substitution`。与 REL-ARTCONC-01-063 和 REL-MATRIX-01-039 相同的问题——合约生成器使用了**四层大括号 `${{{{ }}}}`** 而非正确的两层 `${{ }}`。所有 20 个 job 均因 bash 语法错误直接退出（exit code 1），未执行任何 matrix 变量验证逻辑。

- **预期行为**（Phase 01 文本用例 `REL-MATRIX-01-038`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 4 维×5 值=20 组合的 matrix workflow"
  - 预期结果: "20 个 jobs 全部生成；每个实例获得正确的矩阵变量值；20 个 jobs 全部 completed(success)"
  - 验证点: "[正向] 20 个 jobs 全部生成；[正向] 矩阵变量校验 100% 通过；[负向] 不应出现重复组合或遗漏组合"

- **实际行为**:
  - 20 个 jobs 确实被平台生成（说明 matrix 展开机制工作正常）
  - 但每个 job 的 shell 脚本在第一步就因 `${{{{ matrix.os }}}}: bad substitution` 语法错误崩溃
  - 未执行任何矩阵变量校验——每个实例获得的实际矩阵值无人知晓

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `matrix 20 combos test` job 的 shell 步骤使用了 `os=${{{{ matrix.os }}}}` 引用矩阵变量
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/configure-matrix-builds.md` 中 matrix 变量在 `steps.run` 中的引用语法。规格描述通过 `${{ matrix.os }}` 在 shell 中访问矩阵上下文——**两层大括号**。测试 YAML 中的 `${{{{ }}}}` 四括号违反规格。

**置信度**: 高（合约生成缺陷——`${{{{ }}}}` 四括号语法错误是已知的系统性问题，影响多条 matrix 和表达式用例；20 个 job 全部报同一错误，平台 matrix 展开机制本身正常工作）

**影响**:
- **阻塞性**: ⚪无影响 — 平台大规模matrix展开机制正常（20个job实例均被正确生成），失败仅因合约模板中CI表达式语法错误
- **静默性**: 🟡可察觉 — bash明确报 `bad substitution` 错误，可诊断但非平台问题
- **影响面**: 🟢单用例 — 仅影响使用 `${{{{ }}}}` 四括号模板生成的用例，不影响平台正常功能
- **综合**: 合约生成器四层大括号语法错误导致20个job全部bash崩溃，平台matrix展开机制正常，修复合约生成器模板即可完全规避
- **是否有规避手段**: 是 — 修复合约生成器将 `${{{{ matrix.os }}}}` 改为 `${{ matrix.os }}`

**建议**:
- 修复合约生成器，确保 CI 表达式变量输出为 `${{ matrix.os }}` 而非 `${{{{ matrix.os }}}}`
- 相关用例: REL-ARTCONC-01-063, REL-MATRIX-01-039, REL-OUTPUT-01-016
