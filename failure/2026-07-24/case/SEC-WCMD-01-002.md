## 失败分诊 · SEC-WCMD-01-002 · 跨运行 artifact 必须被视为不可信数据

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "auto_executed"，未出现（PASS）；assertions[1] (positive, run_status) — 期望 equals "completed"，实际 run_status=FAILED，依赖制品不存在导致 job 失败

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（13 行）:
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
  日志显示 download-artifact 插件尝试从当前 workflow（id: e1a87059abb6433e8824fd994031f936）下载名为 "untrusted-artifact" 的制品，但 Found 0 artifact(s)。错误信息明确："Artifact 'untrusted-artifact' not found. Available artifacts: (none)"。这是一个前置条件失败——测试依赖的制品从未被创建（需要一个 fork PR 的不可信运行先上传该 artifact），而非安全机制失败。

- **预期行为**（Phase 01 文本用例 `SEC-WCMD-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个不可信运行（fork PR）上传 artifact"
  - 操作步骤 2: "提交一个特权运行尝试下载并执行该 artifact"
  - 预期结果: "特权运行不自动执行 artifact 内容；artifact 来源可追溯至其产出运行的信任级别"
  - 验证点: "[负向] 不可信来源的 artifact 绝不应被特权运行隐式信任执行"

- **实际行为**:
  - download-artifact 因制品不存在而失败——前置条件"fork PR 已上传 artifact"未被满足
  - 不是 artifact trust boundary 安全机制被绕过——而是 artifact 根本不存在，整个信任边界测试从未进入
  - 步骤 2（Do not auto execute）因步骤 1 失败而未执行

- **失败传导链**: download-artifact 查找 "untrusted-artifact" → Found 0 → `::error::` 抛出 → Job FAILED → step 2 "Do not auto execute" 被跳过

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `artifact-trust` job 的步骤:
    ```yaml
    - name: Download untrusted artifact
      uses: download-artifact
      with:
        name: untrusted-artifact
    - name: Do not auto execute
      run: |
        echo "Artifact downloaded but not executed automatically"
    ```
  - 这对应 GitCode 规格 `writing-pipelines/upload-download-artifacts.md` 第 79-93 行的下载制品配置:
    ```yaml
    steps:
      - name: Download artifact
        uses: download-artifact
        with:
          name: app-dist
          path: dist/
    ```
    以及第 90-93 行的参数表:
    ```
    | name | 是 | 要下载的制品名称 |
    | path | 否 | 下载目标路径，默认为当前工作目录 |
    ```
    规格第 92 行要求 `name` 为必填参数且必须匹配已存在的制品名称。测试中的 "untrusted-artifact" 在当前 workflow 中不存在，平台正确返回了 "not found" 错误——这是正确的平台行为，证明 download-artifact 不会创建虚构的制品。
  - 同时对应 `security-permissions/using-secrets.md` 第 68-71 行的 Fork 隔离机制，文档描述了 fork PR 的隔离原则，但跨 artifact 信任边界是更广义的安全关注。

**置信度**: 高（制品不存在是确凿事实——"Found 0 artifact(s)"——非安全缺陷，是测试前置条件未被满足的用例问题）

**影响**:
- **阻塞性**: ⚪无影响 — 测试前置条件（fork PR 已上传 "untrusted-artifact"）未满足，download-artifact 正确返回 "Artifact not found"，非 artifact trust boundary 安全缺陷
- **静默性**: 🟢明确报错 — 日志明确输出 `::error::Unable to download artifact(s): Artifact 'untrusted-artifact' not found. Available artifacts: (none)`，诊断信息清晰
- **影响面**: 🟢单用例 — 仅影响 SEC-WCMD-01-002 的跨 artifact 信任边界测试
- **综合**: 前置条件缺失导致测试流程被阻断，平台的 download-artifact 行为正确（不会创建虚构制品），非安全漏洞
- **是否有规避手段**: 是 — 需前置步骤创建 "untrusted-artifact"（通过 fork PR workflow run 上传），然后特权 run 尝试下载

**建议**:
- 前置条件需要先执行 fork PR workflow run 来创建 "untrusted-artifact"，然后特权 workflow run 尝试下载
- 若跨 workflow run 的 artifact 下载不被支持（download-artifact 仅限同 workflow），则需重新设计测试——通过 API curl 直接下载其他 run 的 artifact
- 相关用例: SEC-ARTF-01-001, SEC-ARTF-01-002
