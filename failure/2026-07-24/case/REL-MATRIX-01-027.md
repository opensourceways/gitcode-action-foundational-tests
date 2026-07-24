## 失败分诊 · REL-MATRIX-01-027 · matrix max-parallel=4——9 个组合应最多同时运行 4 个

**判定结果**: FAIL
**失败断言**: 正向/max_concurrent_jobs le=4 actual=N/A; 正向/run_status expected=completed(success) actual=N/A (仅 3/9 job 有 log)

**根因初判**: 用例问题（matrix 仅 1 维 3 值，非 3x3=9 组合）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（仅 3 个 job instances）:
  ```
  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:25.955 GMT+08:00] [INFO] Job(1529979528439144448_1529979528447533059) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ef5c5c7a-e84d-43df-aae2-0ad4ab23cd31.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ef5c5c7a-e84d-43df-aae2-0ad4ab23cd31.sh
  version=1

  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:25.842 GMT+08:00] [INFO] Job(1529979528439144448_1529979528447533058) duration check: true
  ...
  version=2

  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:26.346 GMT+08:00] [INFO] Job(1529979528439144448_1529979528447533057) duration check: true
  ...
  version=3
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤: 触发含 3x3 matrix 且 max-parallel=4 的 workflow
  - 预期结果: 任意时刻 in_progress 矩阵 job 数 <=4; 9 个 jobs 全部 completed(success)

- **实际行为**:
  - 仅 3 个 job instances 执行（version=1,2,3），全部 success
  - Phase 01 文本描述 "3x3 matrix = 9 个组合"，但 test YAML 中 matrix 仅有 1 维 `version: [1,2,3]`（3 个值），非 3x3
  - max-parallel=4 对于仅 3 个组合无实际意义——所有 3 个可以同时运行
  - **失败传导链**: Phase 01 文本与 test YAML 不一致 → 仅 3 个组合而非 9 个 → 无法验证 max-parallel 在 9 组合下的行为

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 strategy:
    ```yaml
    strategy:
      matrix:
        version: [1, 2, 3]
      max-parallel: 4
    ```
  - **测试 YAML** 中 `test` 的 step:
    ```yaml
    - name: matrix step
      run: |
        echo version=${{ matrix.version }}
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 46-53 行（一维矩阵示例）:
    ```yaml
    strategy:
      matrix:
        node-version: [18, 20, 22]
    ```
  - **GitCode 规格** `writing-pipelines/configure-matrix-builds.md` 第 123-130 行（max-parallel）:
    ```yaml
    strategy:
      max-parallel: 4
    ```
    限制同时运行的矩阵 job 实例数量
  - **逐项映射**: `matrix.version: [1,2,3]` → 匹配一维矩阵格式（3 值）; `max-parallel: 4` → 匹配规格; `echo version=${{ matrix.version }}` → 匹配表达式格式。但 YAML 生成 3 个实例而非 9 个——与 Phase 01 文本中的 "3x3 matrix = 9" 描述不一致。

- **环境前置条件验证**: runner 可用，3 个 jobs 均成功执行

**置信度**: 高（Phase 01 文本描述 3x3=9 组合，YAML 仅 1 维 3 值 = 3 组合，确切不一致）

**影响**:
- **阻塞性**: 🟡中等 — 用例目的（max-parallel=4 控制 9 组合）未能被测试
- **静默性**: 🟢明确 — 3 个 jobs 成功但未覆盖完整场景
- **影响面**: 🟡同用例 — 仅此矩阵用例
- **综合**: Phase 01 文本与 test YAML 矩阵维度不匹配——文本要求 3x3 matrix，YAML 仅有 1 维 3 值
- **是否有规避手段**: 是（将 matrix 改为二维：添加第二个维度如 `os: [ubuntu, euler, debian]` 使其生成 3x3=9 组合）

**建议**:
- Phase 01 修正：在 YAML 中将 matrix 改为二维 3x3 = 9 组合：
  ```yaml
  matrix:
    version: [1, 2, 3]
    os: [ubuntu, euler, debian]
  ```
- 或修正 Phase 01 文本描述为 "3 个组合" 以匹配实际 YAML
