## 失败分诊 · SEC-RUN-01-003 · 自托管 Runner 跨项目残留必须被隔离

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "cross project leak"，无法验证（无有效日志）；assertions[1] (positive, run_logs) — 期望日志含 "isolated_as_expected"，实际两个 job 均 FAILED 且 0 字节有效步骤输出

**根因初判**: 需人工判断

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: Write project A data (status=FAILED) ===
  [2026/07/23 22:09:54.688 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499271) duration check: true


  === JOB: Check project B isolation (status=FAILED) ===
  [2026/07/23 22:09:54.659 GMT+08:00] [INFO] Job(1529973861045248000_1529973861007499273) duration check: true

  ```
  两个 job 均 FAILED，但日志中没有任何步骤执行痕迹——无 Shell 启动信息、无 `::debug::Script file created` 行、无输出内容。这表明自托管 Runner 可能未能成功分配或启动。两个 job 的 job_id 前缀相同（`1529973861045248000`），表明它们可能被调度到同一 workflow run 中但两个 job 均因 Runner 不可用而直接 FAILED。

- **预期行为**（Phase 01 文本用例 `SEC-RUN-01-003`，优先级 P0，维度 security）:
  - 操作步骤 1: "项目 A 的 workflow 写入临时文件和环境变量"
  - 操作步骤 2: "项目 B 的 workflow 在同一 runner 上检查残留"
  - 预期结果: "项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量；runner 清理失败时应标记为不可用"
  - 验证点: "[负向] 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量"

- **实际行为**:
  - 两个 job 均 FAILED 且无有效步骤输出——步骤脚本从未被创建或执行
  - 无法判断跨项目隔离是否生效——两个 job 都未实际运行过
  - 自托管 Runner 可能不在线、资源不足或调度失败

- **失败传导链**: 自托管 Runner 不可用/调度失败 → job project-a FAILED（无步骤执行）→ job project-b FAILED（无步骤执行）→ 两个断言均无法从空日志中验证

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 使用 `runs-on: [self-hosted, x64, large]` 要求自托管 Runner:
    ```yaml
    project-a:
      name: Write project A data
      runs-on: [self-hosted, x64, large]
    ```
  - 这对应 GitCode 规格 `core-concepts/runner-and-environment.md` 第 30-40 行的自托管资源池说明:
    ```yaml
    jobs:
      self-hosted-build:
        runs-on: [self-hosted, dev-group, linux, x64, gpu]
        steps:
          - run: nvidia-smi
    ```
    规格第 30 行描述了自托管 Runner 的三段式配置 `type/group/labels`。测试 YAML 使用 `[self-hosted, x64, large]` 请求带有 `x64` 和 `large` 标签的自托管 Runner。但 Runner 资源池中可能不存在满足这些标签的可用 Runner。

**置信度**: 低（两个 job 均 0 字节有效日志，无法判断是 Runner 不可用还是平台调度问题；需人工检查自托管 Runner 状态、标签匹配情况和资源池可用性）

**影响**:
- **阻塞性**: 🟡非阻塞 — 两个 job 均 FAILED 但无步骤执行痕迹，自托管 Runner 不可用或调度失败导致测试未执行，非跨项目隔离机制缺陷
- **静默性**: 🟢明确报错 — 两个 job 均 FAILED 状态可观测，但 0 字节有效日志缺乏诊断信息（无 Runner 不可用的明确提示）
- **影响面**: 🟢单用例 — 仅影响 SEC-RUN-01-003（唯一依赖自托管 Runner 的测试用例），不涉及官方 Runner 池
- **综合**: 自托管 Runner 可能不存在（标签 x64 + large 无匹配）或离线，跨项目残留隔离未被实际测试到
- **是否有规避手段**: 是 — 确认自托管 Runner 上线状态和标签匹配，或改用官方 Runner 通过不同 workflow run 模拟跨项目场景

**建议**:
- 检查自托管 Runner 池中是否上线了带有 `x64` 和 `large` 标签的 Runner
- 确认 Runner 的注册状态和心跳是否正常
- 若自托管 Runner 不可用，考虑使用官方 Runner 并调整测试设计（如通过不同的 workflow run 模拟跨项目场景）
- 相关用例: 无（此用例是 SEC-RUN 系列中唯一依赖自托管 Runner 的）
