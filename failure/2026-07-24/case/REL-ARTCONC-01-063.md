## 失败分诊 · REL-ARTCONC-01-063 · 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact

**判定结果**: FAIL
**失败断言**: 正向/download_content expected in=['AAA','BBB','CCC'] actual=所有job因bad substitution未执行; 负向/download_content contains_mixed=false actual=N/A

**根因初判**: 标记不匹配
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（31 行）:
  ```
  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.416] [INFO] Job(1529977680772608000_1529977680780996611) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/19c43dcd-32a8-46d6-bcea-573108e4b7c0.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.320] [INFO] Job(1529977680772608000_1529977680780996610) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.502] [INFO] Job(1529977680772608000_1529977680780996609) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1


  === JOB: artifact concurrent write test (status=FAILED) ===
  ```

- **预期行为**（Phase 01 文本用例 REL-ARTCONC-01-063，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤 1: matrix 3 实例并行，每实例生成不同内容文件并同时 upload-artifact 到同名 artifact
  - 预期结果: 下载内容确定，绝非混合态; 内容完整无损

- **实际行为**:
  - 所有 3 个 matrix 实例均在脚本执行时报 `bad substitution` 错误
  - 原因：YAML 中的 `${{{{ matrix.instance }}}}` 被 runner 解释为 bash 非法替换（四重花括号而非二重）
  - 正确语法应为 `${{ matrix.instance }}`，但 YAML 生成时使用了错误的转义

- **对照 GitCode 规格**:
  - 无直接相关规格段落；GitCode 表达式的正确语法为 `${{ <expression> }}`（二重花括号），Phase 02 YAML 模板生成了 `{{{{ }}}}`（四重花括号）导致 runner 无法正确解析

- **环境前置条件验证**: runner 可用（3 个 job 被调度），但脚本执行立即失败

**置信度**: 高 (bad substitution 错误是明确的模板转义问题)

**影响**:
- **阻塞性**: 🔴阻塞 — 所有 matrix 实例均因相同原因失败
- **静默性**: 🟢明确报错 — `bad substitution` 明确提示
- **影响面**: 🔴跨维度 — 影响所有使用 `{{{{ }}}}` 模板语法的 matrix/expression 用例
- **综合**: Phase 02 YAML 模板将 GitCode 表达式 `${{ }}` 错误转义为 `${{{{ }}}}`，runner 将其解释为 bash 非法操作
- **是否有规避手段**: 是（修正 YAML 模板将 `{{{{ }}}}` 替换为 `${{ }}`）

**建议**:
- Phase 02 修正 YAML 生成模板中的表达式转义逻辑
- 同时修复所有受影响的 REL-MATRIX-01-038、REL-MATRIX-01-039、REL-OUTPUT-01-016 等用例
