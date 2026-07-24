## 失败分诊 · REL-YAMLCACHE-01-060 · Workflow YAML 缓存失效——修改后无旧代码残留

**判定结果**: FAIL
**失败断言**: 正向/run_logs expected=contains "marker_v2" actual=contains "marker_v1"; 负向/run_logs expected=NOT contains "marker_v1" actual=contains "marker_v1"

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: YAML cache invalidation test (status=COMPLETED) ===
  [2026/07/23 22:39:31.470] [INFO] Job(1529981313643851776_1529981313627074567) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  marker_v1
  ```

- **预期行为**（Phase 01 文本用例 REL-YAMLCACHE-01-060，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 修改与触发权限
  - 操作步骤 1: 第一轮执行记录输出 marker_v1
  - 操作步骤 2: 修改 workflow 输出为 marker_v2 并 push
  - 操作步骤 3: 立即触发 workflow
  - 预期结果: 新触发运行日志中出现 marker_v2; 不应出现 marker_v1 缓存残留

- **实际行为**:
  - 日志输出 `marker_v1`，而非预期的 `marker_v2`
  - 这说明第二轮（修改 workflow 为 marker_v2 → push → 触发）未执行，仅执行了第一轮（marker_v1）
  - 也可能第二轮执行了但平台 YAML 缓存未失效，仍返回了旧版 v1 workflow

- **对照 GitCode 规格**:
  - 无直接相关规格段落；此为测试 harness 编排问题，也可能是平台 YAML 缓存机制问题

- **环境前置条件验证**: runner 可用，但二阶段编排（修改 → push → 触发）未执行

**置信度**: 低 (可能是 harness 未执行第二轮，也可能是 platform YAML 缓存确实有问题——需进一步区分)

**影响**:
- **阻塞性**: 🟡非阻塞 — 即使缓存机制有缺陷，不影响基本功能
- **静默性**: 🔴静默错误 — 如果真的是缓存失效问题，用户修改 workflow 后可能运行旧版本
- **影响面**: 🟡同维度 — 影响 workflow 更新流程
- **综合**: 无法判定是 harness 未执行第二轮（环境问题）还是 platform YAML 缓存未失效（平台缺陷），需进一步排查
- **是否有规避手段**: 是（harness 增加二阶段编排，或检查 platform 缓存刷新机制）

**建议**:
- 首先确认 harness 是否执行了第二步（修改 workflow YAML → commit → push → 触发新 run）
- 如果是 platform 缓存问题，需排查 workflow YAML 缓存失效策略
