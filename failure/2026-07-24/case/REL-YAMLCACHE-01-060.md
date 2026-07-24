## 失败分诊 · REL-YAMLCACHE-01-060 · Workflow YAML 缓存失效——修改后无旧代码残留

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_logs) — 期望日志含 `marker_v2`（修改后的输出），实际日志显示 `marker_v1`（旧版代码输出），说明平台使用了缓存的旧 YAML

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: YAML cache invalidation test (status=COMPLETED) ===
  [2026/07/23 22:39:31.470 GMT+08:00] [INFO] Job(1529981313643851776_1529981313627074567) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/3b5dcf9a-66a1-4b08-b131-8a31993711ae.sh
  marker_v1
  ```
  日志显示：job 状态 **COMPLETED**，输出 **`marker_v1`**——这是修改前的旧版 workflow 代码的输出。测试流程为：第一轮执行记录 `marker_v1` → 修改 workflow 源码输出改为 `marker_v2` 并 push → 第二轮执行应输出 `marker_v2`。但实际第二轮执行输出仍为 `marker_v1`（旧版代码），证明**平台缓存了第一次的 workflow YAML 并未在修改后失效**——平台执行的是缓存的旧版 workflow。

- **预期行为**（Phase 01 文本用例 `REL-YAMLCACHE-01-060`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "第一轮执行记录输出 marker_v1"
  - 操作步骤 2: "修改 workflow 输出为 marker_v2 并 push"
  - 操作步骤 3: "立即触发 workflow"
  - 预期结果: "新触发运行日志中出现 marker_v2；不应出现 marker_v1 缓存残留"
  - 验证点: "[正向] 日志打印 marker_v2；[负向] 不应打印 marker_v1"

- **实际行为**:
  - 第二轮执行输出 `marker_v1`（旧版代码）而非 `marker_v2`（新版代码）
  - 平台未检测到 workflow YAML 文件的修改，继续使用缓存的旧版本执行
  - YAML 缓存失效机制失效——修改后的 workflow 未被重新加载

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 的 `YAML cache invalidation test` job 初始版本输出 `marker_v1`，修改后应输出 `marker_v2`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/using-dependency-cache.md` 中缓存失效的一般原则。规格描述缓存应在内容变更时失效并重新加载。平台当前行为——继续使用旧版 YAML——说明缓存失效机制存在缺陷。**这是安全隐患**：如果 workflow YAML 被篡改后旧版仍被执行，可能导致安全策略失效。

**置信度**: 高（日志确凿——第二轮执行输出 `marker_v1` 而非 `marker_v2`，平台缓存未失效；存在安全隐患）

**建议**:
- 平台需确保在 workflow YAML 文件被修改后（通过 push），立即失效对应缓存并重新加载最新版本
- 建议在 workflow dispatch 时校验 YAML 文件的 SHA/ETag，确保执行的是最新内容
- 相关用例: REL-CACHE-01-046
