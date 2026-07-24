## 失败分诊 · REL-MATRIX-01-039 · 大规模 matrix——50 个组合应全部生成并正确调度

**判定结果**: FAIL
**失败断言**: 正向/generated_jobs_count expected=50 actual=N/A; 非功能/scheduling_latency_seconds le=300 actual=N/A

**根因初判**: 用例问题（YAML 模板变量花括号嵌套错误——同 REL-ARTCONC-01-063 / REL-MATRIX-01-038）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（50 个 job instances，全部相同错误，仅展示第 1 个）:
  ```
  === JOB: matrix 50 combos test (status=FAILED) ===
  [2026/07/23 22:32:53.743 GMT+08:00] [INFO] Job(1529979624610467840_1529979624618856486) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/bc0a3896-6449-4bde-abd5-4b3ad88d8a81.sh: line 1: v1=${{{{ matrix.v1 }}}}: bad substitution
  ::error::Process exited with code 1
  ```
  （所有 50 个 job instances 完全相同错误：`${{{{ matrix.v1 }}}}: bad substitution`）

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发含 5 维x10 值=50 组合的 matrix workflow
  - 预期结果: 50 个 jobs 全部生成; 无重复/遗漏组合; 调度时延 <=300 秒

- **实际行为**:
  - 平台正确生成 50 个 job instances（5x10=50 匹配）
  - 所有 instance 在 bash 执行时因 `${{{{ matrix.v1 }}}}` bad substitution 立即失败
  - 同 REL-ARTCONC-01-063 / REL-MATRIX-01-038 的模板渲染问题
  - **失败传导链**: 同模板错误 → 全部 50 instances FAILED → 所有断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 strategy matrix:
    ```yaml
    strategy:
      matrix:
        v1: [a,b,c,d,e]
        v2: [1,2,3,4,5,6,7,8,9,10]
    ```
  - **测试 YAML** 中 `test` 的 verify step:
    ```yaml
    - name: verify matrix vars
      run: |
        echo v1=${{{{ matrix.v1 }}}} v2=${{{{ matrix.v2 }}}}
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 56-63 行:
    ```yaml
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [18, 20]
    ```
  - **逐项映射**: matrix 定义正确（5x10=50 组合，匹配文本描述）; 表达式 `${{ matrix.v1 }}` 规格标准两层花括号，测试 YAML 渲染后为四层。与 REL-ARTCONC-01-063、REL-MATRIX-01-038 完全相同的系统性问题。

- **环境前置条件验证**: runner 可用（50 个 job 均被调度），但所有均在 bash 解析阶段失败

**置信度**: 高（与其他 matrix 用例相同根因——模板渲染花括号层级错误）

**影响**:
- **阻塞性**: 🔴阻塞 — 全部 50 个 jobs 均失败
- **静默性**: 🟢明确报错 — `bad substitution`
- **影响面**: 🔴跨用例 — 与 REL-ARTCONC-01-063、REL-MATRIX-01-038 相同根因，影响所有使用 `{{ matrix.* }}` 的 REL 用例
- **综合**: 模板引擎系统性渲染多一层花括号——需统一修复
- **是否有规避手段**: 是（修复模板渲染后统一去重花括号）

**建议**:
- Phase 01 模板引擎全局修复：`{{ matrix.<var> }}` 在渲染为 `${{ matrix.<var> }}` 后不应再被 YAML 模板包裹一层花括号
- 排查所有 REL 用例中的 matrix 变量引用，已知受影响的：REL-ARTCONC-01-063, REL-MATRIX-01-038, REL-MATRIX-01-039
