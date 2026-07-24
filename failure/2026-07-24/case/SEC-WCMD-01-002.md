## 失败分诊 · SEC-WCMD-01-002 · 跨运行 artifact 必须被视为不可信数据

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "auto_executed"` — **PASS**: 未出现 auto_executed
  - 正向 `run_status` `equals: "completed"` — **FAIL**: download-artifact 失败（artifact not found），job 进入错误状态

**根因初判**: 环境问题（测试 fixture 中的 "untrusted-artifact" 不存在，跨运行边界未正确设置）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
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

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库支持 artifact 传递
  - 操作步骤: 1. 不可信运行（fork PR）上传 artifact；2. 特权运行尝试下载并执行该 artifact
  - 预期结果: 特权运行不自动执行 artifact 内容；artifact 来源可追溯至其产出运行的信任级别

- **实际行为**:
  - `run-id input: '' (length: 0)` — 未指定 run-id，默认使用当前 workflow ID
  - 在当前 workflow (e1a87059abb6...) 中搜索 "untrusted-artifact" — 找到 0 个
  - 前置的 fork PR 上传 artifact 步骤未执行或在不同 workflow 中
  - **失败传导链**: 不可信来源的 artifact 未创建 → 特权运行中 download-artifact 找不到 → "Available artifacts: (none)" → 测试未达到验证边界

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `artifact-trust` 的 `Download untrusted artifact` 和 `Do not auto execute`:
    ```yaml
    setup:
      repo_fixture: with-artifacts
    jobs:
      artifact-trust:
        name: Test artifact trust boundary
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Download untrusted artifact
            uses: download-artifact
            with:
              name: untrusted-artifact
          - name: Do not auto execute
            run: |
              echo "Artifact downloaded but not executed automatically"
    ```
  - **GitCode 规格** `core-concepts/artifacts-and-cache.md` 第 7-19 行:
    ```yaml
    steps:
      - uses: upload-artifact
        with:
          name: build-output
          path: dist/
      - uses: download-artifact
        with:
          name: build-output
          path: ./app
    ```
  - **逐项映射**:
    - `uses: download-artifact` + `name: untrusted-artifact`: 测试 YAML 使用 artifact action — 匹配规格示例
    - `run-id` 未指定: 测试 YAML 未传递跨运行的 run-id 参数 — download-artifact 默认在当前 workflow 中查找
    - **关键缺陷**: 跨运行 artifact 信任测试需要两个独立的 workflow 运行：(1) 不可信运行上传；(2) 特权运行下载 — 当前测试 YAML 仅包含下载端，未设置跨运行引用

- **环境前置条件验证**: fork PR 上传的 artifact 不存在（不可信运行未触发或未产生 artifact）

**置信度**: 高（artifact 不存在，跨运行边界未建立）

**影响**:
- **阻塞性**: 高 — 测试核心流程缺失前置步骤
- **静默性**: 高 — 错误 "not found" 掩盖了信任边界验证
- **影响面**: 中 — 跨运行 artifact 信任是 CI/CD 供应链安全关键
- **综合**: "untrusted-artifact" 在当前 workflow 中不存在（0 artifact），跨运行下载未指定 `run-id` 参数，测试无法验证不可信来源 artifact 的信任边界
- **是否有规避手段**: 是 — 需两阶段测试：(1) 触发不可信运行上传 artifact；(2) 特权运行下载时指定不可信运行的 run-id

**建议**:
- Phase 01/02: 重新设计测试流程为两阶段：(1) Phase 1 workflow（不可信触发）上传 artifact 并记录 run-id；(2) Phase 2 workflow（特权触发）用 `run-id` 参数指定下载不可信运行的 artifact；(3) 验证下载后不自动执行
- Phase 02: 测试 YAML 中 `download-artifact` 增加 `run-id: ${{ needs.untrusted_run.outputs.run_id }}` 或类似跨运行引用
