## 失败分诊 · REL-MATRIX-01-027 · matrix max-parallel=4——9 个组合应最多同时运行 4 个

**判定结果**: FAIL
**失败断言**: 正向/max_concurrent_jobs ≤4 actual=3(满足); 正向/run_status expected=completed(success) actual=3个job COMPLETED但断言期望9个

**根因初判**: 标记不匹配
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（25 行）:
  ```
  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:25.955] [INFO] Job(1529979528439144448_1529979528447533059) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ef5c5c7a-e84d-43df-aae2-0ad4ab23cd31.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ef5c5c7a-e84d-43df-aae2-0ad4ab23cd31.sh
  version=1

  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:25.842] [INFO] Job(1529979528439144448_1529979528447533058) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/7b830982-6c75-4913-8212-a872c4870154.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/7b830982-6c75-4913-8212-a872c4870154.sh
  version=2

  === JOB: matrix test job (status=COMPLETED) ===
  [2026/07/23 22:32:26.346] [INFO] Job(1529979528439144448_1529979528447533057) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/09b98e13-4327-408a-9754-da0dd75e9c90.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/09b98e13-4327-408a-9754-da0dd75e9c90.sh
  version=3

  === JOB: matrix test job (status=COMPLETED) ===
  ```

- **预期行为**（Phase 01 文本用例 REL-MATRIX-01-027，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发含 3x3 matrix 且 max-parallel=4 的 workflow
  - 预期结果: 任意时刻 in_progress 的 matrix job 数 ≤4; 前 4 个完成后自动启动后续 jobs

- **实际行为**:
  - 仅生成了 3 个 matrix job 实例（version=1,2,3），全部 COMPLETED
  - Phase 01 文本用例描述的是 "3x3 matrix"（应产生 9 个组合），但 Phase 02 生成的 YAML 仅定义了 1 维 3 值的 matrix `{version: [1,2,3]}`
  - YAML 中 `max-parallel: 4` 对 3 个 job 无约束效果，与预期 9 个 job 中最多 4 个并发的测试场景不符

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 无直接相关规格段落；3x3 matrix 应是 2 维各 3 值的笛卡尔积（9 组合）

- **环境前置条件验证**: runner 可用，matrix 展开和调度正常（3 个 job 成功执行）

**置信度**: 高 (YAML 中的 matrix 定义与文本用例不一致：1维3值 vs 2维各3值)

**影响**:
- **阻塞性**: 🟡非阻塞 — 每个 job 单独执行正常，但测试覆盖不全（3 个 vs 9 个）
- **静默性**: 🔴静默错误 — 3 个 job 全部成功通过了 concatency≤4 的断言，实际未测试到真正的并发限制
- **影响面**: 🟢单用例 — 仅影响本用例
- **综合**: YAML template 仅实现了 1 维 3 值的 matrix 而非文本描述的 3x3 矩阵，max-parallel=4 约束未实际生效
- **是否有规避手段**: 是（修正 YAML 为 2 维 matrix，如 `{os: [ubuntu,centos,euler], version: [1,2,3]}`）

**建议**:
- Phase 02 将 YAML 中的 matrix 定义修正为 3x3（2 维各 3 值），使实例总数达到 9
- 重新审视 Phase 01 文本用例到 Phase 02 YAML 的转换流程，确保 matrix 维度定义一致
