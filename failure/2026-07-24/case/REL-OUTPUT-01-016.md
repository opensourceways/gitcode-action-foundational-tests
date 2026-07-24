## 失败分诊 · REL-OUTPUT-01-016 · step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 成功读取 1MB output，实际 job status=FAILED；assertions[1] (positive, run_logs) — 期望日志含 1,048,576 bytes 校验通过，实际不存在

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 11 行）:
  ```
  === JOB: output boundary test (status=FAILED) ===
  [2026/07/23 22:34:54.252 GMT+08:00] [INFO] Job(1529980150802427904_1529980150785650695) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/42f50706-2c32-43de-a658-e4a94d1a9b16.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/42f50706-2c32-43de-a658-e4a94d1a9b16.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh: line 1: ${{{{ steps.writer.outputs.data }}}}: bad substitution
  ::error::Process exited with code 1
  ```
  日志显示：**step_1**（写 output）正常执行（无错误输出），但 **step_2**（读 output）在 bash 第一行就报错——`${{{{ steps.writer.outputs.data }}}}: bad substitution`。与 REL-ARTCONC-01-063、REL-MATRIX-01-038/039 相同的根因——合约生成器使用了**四层大括号 `${{{{ }}}}`** 而非正确的两层 `${{ }}`。steps context 引用 `steps.writer.outputs.data` 未在 CI 表达式层正确解析，bash 无法处理此语法。

- **预期行为**（Phase 01 文本用例 `REL-OUTPUT-01-016`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "job 的 step A 向 ATOMGIT_OUTPUT 写入恰好 1 MB 参数"
  - 操作步骤 2: "step B 读取该参数"
  - 预期结果: "step B 读取到完整 1 MB 内容；MD5 校验通过"
  - 验证点: "[正向] 下游读取内容长度=1,048,576 bytes；[负向] 不应截断或丢失"

- **实际行为**:
  - step_1 静默执行（写入 1MB 到 ATOMGIT_OUTPUT），但无输出验证写入是否成功
  - step_2 在 bash 语法层崩溃——`${{{{ steps.writer.outputs.data }}}}: bad substitution`，output 读取完全未执行
  - 1MB 写入和 MD5 校验均未被测试

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `output boundary test` job 的 step_2 使用了 `${{{{ steps.writer.outputs.data }}}}` 引用 step output
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/pass-output-between-jobs.md` 中 step output 的引用语法。规格使用 `${{ steps.writer.outputs.data }}`（两层大括号）访问 step 输出。用例中的 `${{{{ }}}}` 四括号违反规格。

**置信度**: 高（合约生成缺陷——`${{{{ }}}}` 四括号语法错误是已知的系统性问题；bash 语法错误 `bad substitution` 阻断所有 output 读取逻辑）

**建议**:
- 修复合约生成器，确保 steps context 引用输出为 `${{ steps.writer.outputs.data }}` 而非 `${{{{ steps.writer.outputs.data }}}}`
- 相关用例: REL-ARTCONC-01-063, REL-MATRIX-01-038, REL-MATRIX-01-039
