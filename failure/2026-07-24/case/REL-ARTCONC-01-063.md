## 失败分诊 · REL-ARTCONC-01-063 · 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 success，实际所有 matrix job 均 FAILED；assertions[1] (positive, run_logs) — 期望日志含下载内容确定，实际无业务逻辑执行

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 31 行）:
  ```
  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.416 GMT+08:00] [INFO] Job(1529977680772608000_1529977680780996611) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.320 GMT+08:00] [INFO] Job(1529977680772608000_1529977680780996610) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.502 GMT+08:00] [INFO] Job(1529977680772608000_1529977680780996609) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/worksers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  ```
  日志显示：3 个 matrix 实例 job 全部在 bash 执行脚本的第一行就报错 `${{{{ matrix.instance }}}}: bad substitution`——shell 脚本中使用了**四层大括号 `${{{{ }}}}`** 而非正确的两层 `${{ }}`。这是用例生成阶段的合约模板错误，导致 CI 表达式变量 `matrix.instance` 未被渲染就被传给 bash，bash 将其解释为非法变量替换。所有 job 均未执行任何业务逻辑（无 upload-artifact 步骤输出）。

- **预期行为**（Phase 01 文本用例 `REL-ARTCONC-01-063`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "matrix 3 实例并行，每实例生成不同内容文件并同时 upload-artifact 到同名 artifact"
  - 预期结果: "下载内容确定，绝非混合态；内容完整无损"
  - 验证点: "[正向] 下载内容确定；[负向] 不应出现 ABA/BAB 等混合态"

- **实际行为**:
  - 3 个 matrix job 在 bash 层全部因 `${{{{ matrix.instance }}}}: bad substitution` 语法错误直接失败（exit code 1），upload-artifact 步骤从未执行。
  - 制品并发写入逻辑完全未被测试到。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `artifact concurrent write test` job 的 shell 步骤: 在 run 脚本中使用了 `${{{{ matrix.instance }}}}` 引用 matrix 变量
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/expressions.md` 定义的表达式语法 `${{ <expression> }}`。规格明确使用**两层**大括号，而用例合约生成器错误地渲染了**四层**大括号 `${{{{ }}}}`，违反规格语法。

**置信度**: 高（合约生成缺陷——`${{{{ }}}}` 四括号语法错误是已知的系统性问题，影响多条涉及 CI 表达式变量的用例，bash 无法解析此语法，行为与规格完全矛盾）

**影响**:
- **阻塞性**: ⚪无影响 — 平台matrix展开和调度机制工作正常（3个job实例均被正确生成），失败仅因合约模板中CI表达式语法错误
- **静默性**: 🟡可察觉 — bash明确报 `bad substitution` 错误，可诊断但非平台问题
- **影响面**: 🟢单用例 — 仅影响使用 `${{{{ }}}}` 四括号模板生成的用例，不影响平台正常功能
- **综合**: 合约生成器四层大括号语法错误导致bash崩溃退出，平台功能正常，修复合约生成器模板即可完全规避
- **是否有规避手段**: 是 — 修复合约生成器将 `${{{{ }}}}` 改为 `${{ }}`

**建议**:
- 修复合约生成器，确保 CI 表达式变量输出为正确的 `${{ matrix.instance }}` 格式（两层大括号）
- 相关用例: REL-MATRIX-01-038, REL-MATRIX-01-039, REL-OUTPUT-01-016
