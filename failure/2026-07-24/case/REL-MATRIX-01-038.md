## 失败分诊 · REL-MATRIX-01-038 · 大规模 matrix——20 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: 正向/generated_jobs_count expected=20 actual=N/A; 正向/run_status expected=completed(success) actual=ALL FAILED

**根因初判**: 用例问题（YAML 模板变量花括号嵌套错误——同 REL-ARTCONC-01-063）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（20 个 job instances，全部相同错误）:
  ```
  === JOB: matrix 20 combos test (status=FAILED) ===
  [2026/07/23 22:32:39.979 GMT+08:00] [INFO] Job(1529979577273552896_1529979577281941515) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/182b9ee5-b714-401b-a6e2-774ffcef5788.sh: line 1: os=${{{{ matrix.os }}}}: bad substitution
  ::error::Process exited with code 1
  ```
  （所有 20 个 job instances 完全相同错误：`${{{{ matrix.os }}}}: bad substitution`）

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发含 4 维x5 值=20 组合的 matrix workflow
  - 预期结果: 20 个 jobs 全部生成并 success; 每个实例获得正确 matrix 变量值

- **实际行为**:
  - 平台正确生成 20 个 job instances（2x2x2x3=24... wait, 4维=os(2) x arch(2) x compiler(2) x mode(3) = 24, 但文本说20——存在不一致）
  - 所有 instance 在 bash 执行时因 `${{{{ matrix.os }}}}` bad substitution 立即失败
  - 与 REL-ARTCONC-01-063 相同模板渲染问题：表达式被渲染为四层花括号
  - **失败传导链**: 模板变量嵌套 → 所有 instance FAILED → 所有断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 strategy matrix:
    ```yaml
    strategy:
      matrix:
        os: [ubuntu, euler]
        arch: [x64, arm64]
        compiler: [gcc, clang]
        mode: [debug, release, profile]
    ```
  - **测试 YAML** 中 `test` 的 verify step:
    ```yaml
    - name: verify matrix vars
      run: |
        echo os=${{{{ matrix.os }}}} arch=${{{{ matrix.arch }}}} compiler=${{{{ matrix.compiler }}}} mode=${{{{ matrix.mode }}}}
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 56-63 行（二维矩阵示例）:
    ```yaml
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [18, 20]
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 133-142 行:
    ```yaml
    runs-on: ${{ matrix.os }},${{ matrix.arch }},small
    ```
  - **逐项映射**: matrix 定义正确（四维 → 2x2x2x3=24 组合，但文本说 20——组合数不匹配）；表达式格式 `${{ matrix.<var> }}` 在规格中为两层花括号，测试 YAML 渲染后为四层 `${{{{ matrix.<var> }}}}`。与 REL-ARTCONC-01-063 完全相同的模板渲染错误。

- **环境前置条件验证**: runner 可用（所有 20 个 job 均被调度到 runner），但均在 bash 解析阶段失败

**置信度**: 高（同 REL-ARTCONC-01-063——`bad substitution` 是模板渲染的确定性错误）

**影响**:
- **阻塞性**: 🔴阻塞 — 全部 20 个 jobs 均失败
- **静默性**: 🟢明确报错 — `bad substitution` 即时失败
- **影响面**: 🟡同模板 — 影响所有使用 `{{ matrix.* }}` 的 matrix 用例
- **综合**: 模板渲染多一层花括号——Phase 01 YAML 模板中 `{{ matrix.os }}` 渲染后应仅保留 `${{` 包裹，但实际多了两对花括号
- **是否有规避手段**: 是（修复模板嵌套花括号渲染逻辑）

**建议**:
- 与 REL-ARTCONC-01-063 联合修复：模板引擎需检查 `${{ }}` 表达式渲染后的花括号层级
- Phase 01 文本描述 "4维x5值=20" 但 YAML 实际是 2x2x2x3=24——需同步修正文本或 YAML
