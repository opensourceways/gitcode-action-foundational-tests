## 失败分诊 · SEC-INJ-01-005 · 表达式求值必须防止双重模板渲染（二次求值）

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "2"` — **PASS**: 日志中未出现 "2"（即内层 `{{ 1 + 1 }}` 未被求值）
  - 正向 `run_logs` `equals: "template_chars_escaped"` — **FAIL**: 实际输出 `${{ '{{ 1 + 1 }}' }}` 导致 bash "bad substitution" 错误，非正常的转义输出

**根因初判**: 测试 YAML 表达式嵌套写法导致 bash 解释错误
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test double template eval (status=FAILED) ===
  [2026/07/23 22:06:36.637 GMT+08:00] [INFO] Job(1529973030472265728_1529973030451294209) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh: line 1: Input: ${{ '{{ 1 + 1 }}' }}: bad substitution
  ::error::Process exited with code 1
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库支持表达式求值
  - 操作步骤: 1. 提交一个 workflow，在输入中包含模板语法字符（如 `{{ 1 + 1 }}`）；2. 查看运行日志
  - 预期结果: 外层 `${{ }}` 求值结果中的模板语法字符应被转义；不再触发内层模板引擎求值

- **实际行为**:
  - bash 报错 "bad substitution"，退出码 1，job FAILED
  - 表达式 `${{ '{{ 1 + 1 }}' }}` 的嵌套写法导致：外层 `${{ }}` 被平台表达式引擎求值后，结果字符串被传给 bash 解释，bash 将其解释为变量替换语法 `${{ ... }}` 而报错
  - 虽然内层 `{{ 1 + 1 }}` 未被求值为 2（日志无 "2"），但 job 因 bash 错误而失败
  - **失败传导链**: `${{ '{{ 1 + 1 }}' }}` → 平台表达式引擎求值 → 输出 `${{ 1 + 1 }}` → bash 尝试解释 `${{ }}` → bad substitution → exit 1

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `double-template` 的 `Pass template syntax`:
    ```yaml
    steps:
      - name: Pass template syntax
        run: |
          echo "Input: ${{ '{{ 1 + 1 }}' }}"
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 40-45 行:
    ```
    ## Expressions
    Expressions embed into YAML values using `${{ expression }}` syntax:
    **Operators**: `==`, `!=`, `!`, `&&`, `||`
    ```
  - **逐项映射**:
    - `${{ '{{ 1 + 1 }}' }}`: 测试 YAML 使用单引号包裹 `{{ 1 + 1 }}` 作为表达式字面量 — 期望平台求值后输出 `'{{ 1 + 1 }}'` 字符串
    - 规格未定义如何转义表达式内的 `{{` / `}}` 字符，也未说明表达式求值结果传递给 shell 时的行为
    - **问题**: 测试 YAML 的嵌套写法 `${{ '{{ 1 + 1 }}' }}` 在设计上依赖表达式引擎的字符串字面量处理，但求值后结果 `${{ 1 + 1 }}` 在 bash 中仍被解释

- **环境前置条件验证**: 平台表达式引擎正常求值，但输出格式导致 bash 报错

**置信度**: 中（bash 报错清晰，但该行为可能恰好是平台的设计预期——表达式求值后将 `{{ }}` 字面量保留；bash 层面的错误属于 shell 行为，不代表双重模板渲染）

**影响**:
- **阻塞性**: 低 — 可通过修改测试 YAML 中的 echo 字符串避开 bash 误解释
- **静默性**: 中 — 若平台存在二次求值漏洞，当前测试会因 bash 报错而无法发现
- **影响面**: 低 — 仅影响该特定测试用例
- **综合**: 测试 YAML 中的 `${{ '{{ 1 + 1 }}' }}` 写法导致 bash "bad substitution" 错误，而非预期中的"模板字符被安全转义输出"；需改写为不触发 bash 变量替换的写法（如单引号包裹整个 echo 字符串）
- **是否有规避手段**: 是 — 修改 echo 为 `echo 'Input: ${{ 1 + 1 }}'` 或使用 `printf` 避免 bash 解释

**建议**:
- Phase 01: 修正测试用例的表达式测试写法：(1) 使用 `echo 'Input: {{ 1 + 1 }}'` 直接在 YAML 中硬编码模板字符串；(2) 或先用 `${{ }}` 设置环境变量，再由 shell 安全输出
- Phase 02: 修改测试 YAML 的 run 步骤，避免 `${{ }}` 输出残留的 `${{ }}` 被 bash 二次解释
