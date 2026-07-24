## 失败分诊 · REL-OUTPUT-01-016 · step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递

**判定结果**: FAIL
**失败断言**: 正向/step_output_length expected=1048576 actual=read step因bad substitution失败

**根因初判**: 标记不匹配
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（11 行）:
  ```
  === JOB: output boundary test (status=FAILED) ===
  [2026/07/23 22:34:54.252] [INFO] Job(1529980150802427904_1529980150785650695) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/42f50706-2c32-43de-a658-e4a94d1a9b16.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/42f50706-2c32-43de-a658-e4a94d1a9b16.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/a64765c6-bb13-4184-824b-39ae4011cf69.sh: line 1: ${{{{ steps.writer.outputs.data }}}}: bad substitution
  ::error::Process exited with code 1
  ```

- **预期行为**（Phase 01 文本用例 REL-OUTPUT-01-016，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: job 的 step A 向 ATOMGIT_OUTPUT 写入恰好 1 MB 参数
  - 操作步骤 2: step B 读取该参数
  - 预期结果: step B 读取到完整 1 MB 内容; MD5 校验通过

- **实际行为**:
  - step A (writer) 静默执行完毕（无错误输出，说明 1 MB 写入可能成功）
  - step B (reader) 在脚本解析阶段失败：`${{{{ steps.writer.outputs.data }}}}: bad substitution`
  - 与 REL-ARTCONC-01-063 等相同的四重花括号模板转义问题
  - 正确语法应为 `${{ steps.writer.outputs.data }}`

- **对照 GitCode 规格**:
  - 无直接相关规格段落；GitCode 表达式 `steps.<id>.outputs.<name>` 的正确引用方式为 `${{ steps.writer.outputs.data }}`

- **环境前置条件验证**: step A 执行正常，runner 可用，问题仅限于 YAML 表达式转义

**置信度**: 高 (bad substitution 与之前多个 `{{{{ }}}}` 用例完全一致)

**影响**:
- **阻塞性**: 🔴阻塞 — read step 因语法错误无法执行
- **静默性**: 🟢明确报错 — `bad substitution` 明确指示
- **影响面**: 🔴跨维度 — 影响所有使用 `${{{{ }}}}` 的 expression 引用
- **综合**: Phase 02 YAML 模板将 step output 引用错误转义，导致 runner 将 `${{{{ }}}}` 当作 bash 替换而非 GitCode 表达式
- **是否有规避手段**: 是（修正 YAML 模板中 `${{{{ steps.writer.outputs.data }}}}` 为 `${{ steps.writer.outputs.data }}`）

**建议**:
- Phase 02 统一修正所有 YAML 模板中的 expression 转义
- 此问题影响面广，修复后所有相关用例应立即复测
