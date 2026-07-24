## 失败分诊 · REL-ARTCONC-01-063 · 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact

**判定结果**: FAIL
**失败断言**: 正向/download_content expected in ['AAA','BBB','CCC'] actual=N/A; 负向/download_content contains_mixed expected=false actual=N/A

**根因初判**: 用例问题（YAML 模板语法错误）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（全 31 行，所有 job 实例相同错误）:
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
  ...
  /home/slave1/runner/workers/0.0.4.4.version/_temp/e4b01d41-956b-4c3e-9a2e-8ee4218079c1.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1

  === JOB: artifact concurrent write test (status=FAILED) ===
  [2026/07/23 22:25:05.502 GMT+08:00] [INFO] Job(1529977680772608000_1529977680780996609) duration check: true
  ...
  /home/slave1/runner/workers/0.0.4.4.version/_temp/c52b5f3c-c240-4e8c-8218-6b63fe2c82c6.sh: line 1: ${{{{ matrix.instance }}}}: bad substitution
  ::error::Process exited with code 1

  === JOB: artifact concurrent write test (status=FAILED) ===
  （所有 4 个 matrix job 实例均相同错误）
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤: matrix 3 实例并行，每实例生成不同内容文件并同时 upload-artifact 到同名 artifact
  - 预期结果: 下载内容确定，绝非混合态; 内容完整无损

- **实际行为**:
  - 所有 matrix job 实例因 `${{{{ matrix.instance }}}}` bad substitution 立即失败
  - run step 中的表达式使用了四层花括号 `${{{{ matrix.instance }}}}`，应为 `${{ matrix.instance }}`
  - 这导致 job 自身无法执行到 upload-artifact 阶段
  - **失败传导链**: 语法错误 → 所有实例 FAILED → upload 未执行 → 所有断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 `generate content` step:
    ```yaml
    - name: generate content
      run: |
        if [ "${{{{ matrix.instance }}}}" = "1" ]; then python3 -c "print('A'*1048576)" > out.txt; fi
        if [ "${{{{ matrix.instance }}}}" = "2" ]; then python3 -c "print('B'*1048576)" > out.txt; fi
        if [ "${{{{ matrix.instance }}}}" = "3" ]; then python3 -c "print('C'*1048576)" > out.txt; fi
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 21-27 行:
    ```yaml
    jobs:
      test:
        runs-on: ${{ matrix.os }},${{ matrix.arch }},small
        strategy:
          matrix:
            os: [ubuntu-latest, windows-latest]
            arch: [x64]
            node-version: [18, 20]
    ```
  - **GitCode 规格** `syntax-reference/expressions.md` 表达式语法:
    ```yaml
    ${{ matrix.node-version }}
    ```
  - **逐项映射**: 规格中表达式使用双层花括号 `${{ matrix.<var> }}`，而测试 YAML 使用了四层 `${{{{ matrix.instance }}}}`，导致 bash bad substitution 错误。这是 YAML 模板中的双花括号跨层嵌套问题——Phase 01 模板用 `{{` 表示 YAML 模板变量，Phase 02 渲染后应产出 `${{ matrix.instance }}`，但实际产出了 `${{{{ matrix.instance }}}}`（多了一层）。

- **环境前置条件验证**: runner 可调度（所有 instances 均已分配到 runner），但脚本在 bash 执行时立即因 bad substitution 退出

**置信度**: 高（`bad substitution` 是明确的模板渲染错误，无需怀疑平台或环境）

**影响**:
- **阻塞性**: 🔴阻塞 — job 一步也未执行成功
- **静默性**: 🟢明确报错 — `bad substitution` 即时失败
- **影响面**: 🟡同模板 — 影响所有使用 `{{ matrix.<var> }}` 的 matrix 用例
- **综合**: 模板渲染多了一层花括号包裹，导致表达式在 runner 端被 bash 误解为变量替换
- **是否有规避手段**: 是（修复模板嵌套花括号渲染逻辑，确保仅产出 `${{ matrix.instance }}`）

**建议**:
- Phase 01 生成模板时需检查花括号嵌套层级，确保 `${{ }}` 表达式仅两层
- 所有使用 `${{ matrix.* }}` 的 REL 用例应统一排查相同问题
