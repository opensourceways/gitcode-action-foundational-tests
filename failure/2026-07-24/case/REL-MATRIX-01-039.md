## 失败分诊 · REL-MATRIX-01-039 · 大规模 matrix——50 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 50 个 jobs 全部 success，实际所有 job 均 FAILED；assertions[1] (positive, run_logs) — 期望日志含矩阵变量值，实际无任何业务逻辑输出

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 451 行，50 个 job 重复相同错误）:
  ```
  === JOB: matrix 50 combos test (status=FAILED) ===
  [2026/07/23 22:32:53.743 GMT+08:00] [INFO] Job(1529979624610467840_1529979624618856486) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh: line 1: v1=${{{{ matrix.v1 }}}}: bad substitution
  ::error::Process exited with code 1

  === JOB: matrix 50 combos test (status=FAILED) ===
  ...（重复 50 次相同的 bad substitution 错误）...
  ```
  日志显示：**50 个 matrix job 实例全部在 bash 第一行报错**——`v1=${{{{ matrix.v1 }}}}: bad substitution`。与 REL-ARTCONC-01-063 和 REL-MATRIX-01-038 完全相同的根因——合约生成器使用了**四层大括号 `${{{{ }}}}`** 而非正确的两层 `${{ }}`。所有 50 个 job 均因 bash 语法错误直接退出（exit code 1），未执行任何业务逻辑。值得注意的是——平台成功**生成**了 50 个 job 实例（说明大规模 matrix 展开机制工作正常），只是 shell 脚本在运行时崩溃。

- **预期行为**（Phase 01 文本用例 `REL-MATRIX-01-039`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 5 维×10 值=50 组合的 matrix workflow"
  - 预期结果: "50 个 jobs 全部生成；无重复/遗漏组合；调度时延 ≤300 秒"
  - 验证点: "[正向] 50 个 jobs 全部生成；[正向] 无重复/遗漏组合；[非功能] 调度时延 ≤300 秒"

- **实际行为**:
  - 50 个 jobs 确实被平台生成（说明大规模 matrix 调度机制工作正常）
  - 每个 job 的 shell 脚本在第一步就因 `${{{{ matrix.v1 }}}}: bad substitution` 崩溃
  - 无法验证：每个实例获得的实际矩阵值、是否有重复/遗漏、调度时延

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `matrix 50 combos test` job 的 shell 步骤使用了 `v1=${{{{ matrix.v1 }}}}` 引用矩阵变量
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/configure-matrix-builds.md` 中 matrix 上下文变量的访问语法。规格使用 `${{ matrix.v1 }}`（两层大括号），用例中的 `${{{{ }}}}` 四括号违反规格定义。

**置信度**: 高（合约生成缺陷——`${{{{ }}}}` 四括号语法错误是已知的系统性问题；50 个 job 全部报同一 bash 语法错误，平台 matrix 展开和大规模调度机制本身正常工作）

**建议**:
- 修复合约生成器，确保 CI 表达式变量输出为 `${{ matrix.v1 }}` 而非 `${{{{ matrix.v1 }}}}`
- 相关用例: REL-ARTCONC-01-063, REL-MATRIX-01-038, REL-OUTPUT-01-016
