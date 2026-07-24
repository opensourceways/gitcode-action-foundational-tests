## 失败分诊 · REL-OUTPUT-01-016 · step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递

**判定结果**: FAIL
**失败断言**: 正向/step_output_length expected=1048576 actual=N/A

**根因初判**: 用例问题（YAML 模板变量花括号嵌套错误——step 间 outputs 引用渲染失败）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
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

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: job 的 step A 向 ATOMGIT_OUTPUT 写入恰好 1 MB 参数; step B 读取该参数
  - 预期结果: step B 读取到完整 1 MB 内容; MD5 校验通过

- **实际行为**:
  - write 1MB output step 成功执行（无错误输出，`$ATOMGIT_OUTPUT` 写入成功）
  - read step 在 bash 执行时因 `${{{{ steps.writer.outputs.data }}}}` bad substitution 失败
  - 与 matrix 用例相同的模板渲染问题：`{{ steps.writer.outputs.data }}` 在渲染后变成了 `${{{{ steps.writer.outputs.data }}}}`
  - **失败传导链**: write step 成功 → read step 因表达式渲染错误 FAILED → 断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 writer step:
    ```yaml
    - name: write 1MB output
      id: writer
      run: |
        python3 -c "print('A'*1048576)" > out.txt
        echo "data=$(cat out.txt)" >> $ATOMGIT_OUTPUT
    ```
  - **测试 YAML** 中 `test` 的 read step:
    ```yaml
    - name: read 1MB output
      run: |
        echo "${{{{ steps.writer.outputs.data }}}}"
        test $(echo "${{{{ steps.writer.outputs.data }}}}" | wc -c) -ge 1048576
    ```
  - **GitCode 规格** `writing-pipelines/pass-output-between-jobs.md` 第 25-28 行:
    ```yaml
    steps:
      - id: version
        run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
    ```
  - **GitCode 规格** `writing-pipelines/pass-output-between-jobs.md` 第 31-43 行:
    ```yaml
    - id: version
      run: echo "version=1.0.0" >> "$ATOMGIT_OUTPUT"
    ```
  - **逐项映射**: `id: writer` + `echo "data=..." >> $ATOMGIT_OUTPUT` → 匹配规格; `${{ steps.writer.outputs.data }}` 表达式在规格中为标准两层花括号，测试 YAML 渲染后为四层。与 matrix 用例相同的模板渲染问题。

- **环境前置条件验证**: runner 可用，write step 成功；read step 在 bash 解析阶段失败

**置信度**: 高（同 matrix 用例的模板渲染问题——系统性错误而非个别问题）

**影响**:
- **阻塞性**: 🔴阻塞 — read step 一步也无法执行
- **静默性**: 🟢明确报错 — `bad substitution`
- **影响面**: 🔴跨用例 — 与所有使用 `{{ steps.*.outputs.* }}` 的用例相同根因
- **综合**: 模板引擎对 `${{ }}` 表达式的渲染存在系统性多一层花括号问题
- **是否有规避手段**: 是（修复模板花括号嵌套渲染逻辑）

**建议**:
- 与 REL-ARTCONC-01-063/REL-MATRIX-01-038/REL-MATRIX-01-039 联合修复
- 问题不在于某个变量，而是模板渲染引擎对所有 `{{ }}` 表达式都多包裹了一层花括号
- 需要排查 Phase 01 YAML 模板中花括号的嵌套逻辑
