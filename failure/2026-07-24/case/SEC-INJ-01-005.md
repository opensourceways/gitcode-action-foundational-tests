## 失败分诊 · SEC-INJ-01-005 · 表达式求值必须防止双重模板渲染（二次求值）

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "2" — 未出现 "2"，通过
- positive, run_logs, equals "template_chars_escaped" — 实际为 bash bad substitution 错误，不匹配

**根因初判**: 平台缺陷
**责任人**: 平台方

**证据**:

- **Job 日志全量** (7 行):
  ```
  === JOB: Test double template eval (status=FAILED) ===
  [2026/07/23 22:06:36.637 GMT+08:00] [INFO] Job(1529973030472265728_1529973030451294209) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh: line 1: Input: ${{ '{{ 1 + 1 }}' }}: bad substitution
  ::error::Process exited with code 1
  ```

- **预期行为** (Phase 01 文本用例 SEC-INJ-01-005, 优先级 P0, 维度 security):
  - 前置条件: 仓库支持表达式求值
  - 操作步骤 1: 提交一个 workflow，在输入中包含模板语法字符（如 `{{ 1 + 1 }}`）
  - 操作步骤 2: 触发 workflow 并查看运行日志
  - 预期结果: 外层 `${{ }}` 求值结果中的模板语法字符应被转义；不再触发内层模板引擎求值

- **实际行为**:
  - YAML 中 `run: echo "Input: ${{ '{{ 1 + 1 }}' }}"` 未被平台表达式引擎处理
  - `${{ '{{ 1 + 1 }}' }}` 未被展开为转义后的字面量 `{{ 1 + 1 }}`，而是原样传递给 bash
  - bash 无法解析 `${{ }}` 语法，报 `bad substitution` 并退出
  - 说明平台表达式引擎在 `run:` 块中未正确处理嵌套 `{{ }}`

- **对照 GitCode 规格** `core-concepts/variables-secrets-context-expressions.md`:
  - 第 42-43 行: "Expressions embed into YAML values using `${{ expression }}` syntax"
  - 表达式求值应在 YAML 解析阶段完成，不应在 run 块中遗留未处理的 `${{ }}` 语法

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 fault_injection, 无 config_probe。

**置信度**: 高 (bash bad substitution 错误明确指示表达式未被处理)

**影响**:
- **阻塞性**: 🔴阻塞 — 表达式引擎绕过可能导致模板注入攻击
- **静默性**: 🟡可察觉 — bash 报错退出（非静默），但平台层面未检测到异常
- **影响面**: 🔴跨维度 — 表达式求值机制是所有 workflow 的核心基础设施
- **综合**: 平台表达式引擎未在 run 块中处理嵌套 `${{ }}` 表达式，导致 bash 语法错误
- **是否有规避手段**: 否

**建议**:
- 平台修复表达式引擎，在 `run:` 块中正确处理 `${{ '{{ ... }}' }}` 字面量表达式
- 表达式求值后应转义或剥离内层 `{{ }}` 使输出仅为字面字符串
- 测试 YAML 可增加中间环境变量对比：`env: MSG: ${{ '{{ 1 + 1 }}' }}` 然后 `echo "$MSG"`
