## 失败分诊 · REL-RERUN-01-011 · rerun 边界值——单条运行连续重新运行 3 次应全部成功

**判定结果**: FAIL
**失败断言**: 正向/rerun_count expected=3 actual=仅1个run记录; 正向/run_status expected=completed(success) actual=1个run COMPLETED但无法验证3次

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: reliability test job (status=COMPLETED) ===
  [2026/07/23 22:35:44.236] [INFO] Job(1529980360316555264_1529980360291389447) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/63cb090b-59e5-4785-be0e-1f92475aae7e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/63cb090b-59e5-4785-be0e-1f92475aae7e.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-RERUN-01-011，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库存在一次失败的 workflow 运行
  - 操作步骤 1: 对该运行依次执行 Re-run all jobs 共 3 次
  - 预期结果: 第 1-3 次 rerun 均创建新运行; 每次 rerun 的 atomgit.sha/ref 与原始运行一致; 3 次新运行均 success

- **实际行为**:
  - 日志仅显示 1 个 job 完成
  - 未体现 "先失败再 rerun 3 次" 的多阶段流程
  - harness 未执行 rerun 编排逻辑

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/running-pipelines/view-job-logs.md`:
  - 无直接相关规格段落；rerun 测试需 harness 调用 Re-run API

- **环境前置条件验证**: 单个 job 正常，rerun 编排缺失

**置信度**: 中 (仅 1 个 run 日志，rerun 流程明显未执行)

**影响**:
- **阻塞性**: 🔴阻塞 — rerun 功能无法验证
- **静默性**: 🔴静默错误 — rerun 操作未执行
- **影响面**: 🟡同维度 — 影响所有 rerun 相关测试
- **综合**: harness 未实现先失败再 rerun 3 次的编排流程，仅执行了单次 run
- **是否有规避手段**: 是（harness 实现 rerun API 调用和循环编排）

**建议**:
- Phase 02 实现 rerun 测试编排：先触发一次会失败的 run → 通过 API 执行 Re-run all jobs → 重复 3 次 → 验证每次 rerun 的状态
