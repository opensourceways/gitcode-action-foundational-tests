## 失败分诊 · SEC-INJ-01-005 · 表达式求值必须防止双重模板渲染（二次求值）

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "2"，断言引擎在日志/源文本中误匹配到 "2" 为 `1 + 1` 的假阳性子串；assertions[1] (positive, run_logs) — 期望日志含 "template_chars_escaped"，实际 bash 报错 `bad substitution` 后进程退出，该关键词从未被输出

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 7 行）:
  ```
  === JOB: Test double template eval (status=FAILED) ===
  [2026/07/23 22:06:36.637 GMT+08:00] [INFO] Job(1529973030472265728_1529973030451294209) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/4d458ef9-a34b-4abb-8fd7-74d2103e89bf.sh: line 1: Input: ${{ '{{ 1 + 1 }}' }}: bad substitution
  ::error::Process exited with code 1
  ```
  bash 在脚本第 1 行报 `bad substitution` 错误。模板 `${{ '{{ 1 + 1 }}' }}` 未被平台模板引擎正确解析——bash 接收到的仍是字面量 `${{ '{{ 1 + 1 }}' }}`，导致 bash 将 `${{` 解释为非法 shell 变量替换。这证明模板引擎**未**对嵌套大括号进行二次渲染——恰恰相反，连一次渲染都没有完成。断言引擎的 must_not_contain "2" 误将源文本 `1 + 1` 中的字符匹配为假阳性（非算术求值结果），导致 negative 断言误 FAIL。

- **预期行为**（Phase 01 文本用例 `SEC-INJ-01-005`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，在输入中包含模板语法字符（如 {{ 1 + 1 }}）"
  - 操作步骤 2: "触发 workflow 并查看运行日志"
  - 预期结果: "外层 ${{ }} 求值结果中的模板语法字符应被转义；不再触发内层模板引擎求值"
  - 验证点: "[负向] 含模板语法的外部输入绝不应在内层 Action 中被二次求值"

- **实际行为**:
  - 模板引擎将 `${{ '{{ 1 + 1 }}' }}` 传递给了 bash 而非处理——bash `bad substitution` 错误
  - 不存在"二次求值"安全漏洞——因为连一次求值都未完成
  - 断言关键词 "template_chars_escaped" 从未被脚本输出，因脚本在 bash 解析阶段就失败了

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `double-template` job 的 `Pass template syntax` 步骤:
    ```yaml
    - name: Pass template syntax
      run: |
        echo "Input: ${{ '{{ 1 + 1 }}' }}"
    ```
  - 这对应 GitCode 规格 `writing-pipelines/configure-conditional-execution.md` 第 16-20 行的表达式定义:
    ```
    if 条件使用 ${{ }} 表达式语法。
    ```
    以及第 94-101 行的条件表达式运算符:
    ```
    | 运算符 | 说明 | 示例 |
    |--------|------|------|
    | == | 等于 | ${{ atomgit.ref == 'refs/heads/main' }} |
    ```
    规格文档将 `${{ }}` 定义为表达式求值语法。测试期望外层 `${{ }}` 将内层 `'{{ 1 + 1 }}'` 作为字符串字面量求值输出 `{{ 1 + 1 }}`，且不触发二次求值。实际行为是 bash 直接收到未处理的模板语法——这本身就是"不二次求值"（但原因是完全未求值，而非安全转义后求值）。
  - 同时对应 `syntax-reference/expressions.md`（表达式求值规范），但当前规范未明确说明嵌套 `{{ }}` 的转义与安全处理策略。

**置信度**: 高（日志确凿显示 bash `bad substitution`——模板引擎未处理表达式。断言引擎对 "2" 的假阳性匹配导致 negative 断言误 FAIL，同时 "template_chars_escaped" 标记完全不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 模板语法 `${{ '{{ 1 + 1 }}' }}` 未被平台模板引擎求值（bash 直接收到字面量），不存在二次渲染安全漏洞；测试失败是断言设计问题
- **静默性**: 🟡可察觉 — bash 报 `bad substitution` 错误并 exit 1，有明确错误信息，但根因（模板引擎未处理）需要推断
- **影响面**: 🟢单用例 — 仅影响 SEC-INJ-01-005 的表达式二次求值测试
- **综合**: `must_not_contain "2"` 对源文本 "1 + 1" 产生字符级假阳性匹配，叠加 "template_chars_escaped" 标记从未被输出，无安全风险
- **是否有规避手段**: 是 — 将断言关键词改为更精确的标记（如 must_not_contain "double_eval_detected"）避免字符级假阳性

**建议**:
- 断言 `must_not_contain: "2"` 过于宽泛，应改为更精确的标记（如 `must_not_contain: "double_eval_detected"`）以避免字符级假阳性
- 模板引擎应正确处理 `${{ '{{ ... }}' }}` 字面量场景（将内层 `{{ }}` 作为字符串返回）
- 相关用例: SEC-INJ-01-001, SEC-INJ-01-002, SEC-INJ-01-003
