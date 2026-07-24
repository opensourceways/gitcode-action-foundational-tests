## 失败分诊 · SEC-WCMD-01-002 · 跨运行 artifact 必须被视为不可信数据

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "auto_executed" — 通过（未自动执行）
- positive, run_status, equals "completed" — job 状态 FAILED，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (13 行):
  ```
  === JOB: Test artifact trust boundary (status=FAILED) ===
  [2026/07/23 22:11:09.460 GMT+08:00] [INFO] Job(1529974174812868608_1529974174787702791) duration check: true
  ::debug::run-id input: '' (length: 0)
  ::debug::Resolved path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3
  ::debug::Artifact client initialized for https://actions-results.atomgit.com
  ::debug::Resolved workflow id e1a87059abb6433e8824fd994031f936
  Downloading single artifact
  ::debug::Listing artifacts for workflow e1a87059abb6433e8824fd994031f936 with name filter "untrusted-artifact"
  [Twirp] trace-id: f97e8586618b9a46953ce542e8743a45
  ::debug::Found 0 artifact(s)
  ::error::Unable to download artifact(s): Artifact 'untrusted-artifact' not found. Available artifacts: (none)
  
   
  ```

- **预期行为** (Phase 01 文本用例 SEC-WCMD-01-002, 优先级 P0, 维度 security):
  - 前置条件: 仓库支持 artifact 传递
  - 操作步骤 1: 提交一个不可信运行（fork PR）上传 artifact
  - 操作步骤 2: 提交一个特权运行尝试下载并执行该 artifact
  - 预期结果: 特权运行不自动执行 artifact 内容；artifact 来源可追溯至其产出运行的信任级别

- **实际行为**:
  - `download-artifact` 尝试下载名为 `untrusted-artifact` 的 artifact
  - 结果: `Found 0 artifact(s)` — 目标 artifact 不存在
  - `run-id input: '' (length: 0)` — run-id 为空，未正确传递 fork PR 的运行 ID
  - artifact 来源追溯因下载失败而无法验证
  - 失败传导链: 单 job，artifact 不存在导致下载失败

- **对照 GitCode 规格** `core-concepts/workflow-job-step-action.md`:
  - 第 N-M 行: artifact 应可跨运行传递且来源可追溯（信任级别判定）

- **环境前置条件验证**: YAML `setup.repo_fixture: with-artifacts`。假定 fixture 提供了名为 `untrusted-artifact` 的预设 artifact，但实际环境中该 artifact 不存在。`run-id` 输入为空表明跨运行 artifact 追踪机制未正确配置。

**置信度**: 高 (artifact 不存在 + run-id 为空)

**影响**:
- **阻塞性**: 🔴阻塞 — artifact 信任边界验证完全无法执行
- **静默性**: 🟢明确报错 — "Artifact 'untrusted-artifact' not found" 清晰指示
- **影响面**: 🟢单用例 — 仅影响此 artifact 信任边界测试
- **综合**: 测试 fixture 中的 `untrusted-artifact` 未预先创建；run-id 参数为空表明跨运行衔接缺失
- **是否有规避手段**: 是

**建议**:
- 测试 YAML 添加前置步骤：先上传 `untrusted-artifact`（模拟 fork PR 创建）
- 修复 `run-id` 输入：通过 workflow_call 或 inputs 传递不可信运行的 run ID
- 扩展 fixture 为双 workflow 结构：(a) 不可信运行上传 artifact (b) 特权运行下载并检查
- 添加 config_probe 步骤：列出所有可用 artifact 确认 fixture 正确
