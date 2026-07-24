## 失败分诊 · REL-ARTPERF-01-053 · 制品传输性能——100MB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: 非功能/upload_time_seconds le=30 actual=N/A; 非功能/download_time_seconds le=30 actual=N/A; 正向/hash_match expected=true actual=false

**根因初判**: 用例问题（验证 step 中 artifact 解压路径不匹配）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: upload artifact job (status=COMPLETED) ===
  [2026/07/23 22:25:15.777 GMT+08:00] [INFO] Job(1529977724519452672_1529977724494286855) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c5c59c65-3e0e-47f1-88b4-5ee920e9f8fb.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c5c59c65-3e0e-47f1-88b4-5ee920e9f8fb.sh
  100+0 records in
  100+0 records out
  104857600 bytes (105 MB, 100 MiB) copied, 0.332445 s, 315 MB/s

  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Uploading artifact "perf-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ...
  Artifact "perf-artifact" uploaded successfully. ID: 206054130524160, Size: 104889728 bytes

  === JOB: download artifact job (status=FAILED) ===
  [2026/07/23 22:25:36.143 GMT+08:00] [INFO] Job(1529977724519452672_1529977724494286857) duration check: true
  ::debug::run-id input: '' (length: 0)
  ::debug::Resolved path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  ::debug::Artifact client initialized for https://actions-results.atomgit.com
  ::debug::Resolved workflow id 37377f8b2720406ca6780f11c1fe26ed
  Downloading single artifact
  ::debug::Listing artifacts for workflow 37377f8b2720406ca6780f11c1fe26ed with name filter "perf-artifact"
  [Twirp] trace-id: 824eaa2a3e6751b13cae333dd90733ae
  ::debug::Found 1 artifact(s)
  ::debug::Found named artifact 'perf-artifact' (ID: 206054130524160, Size: 104889728)
  Preparing to download the following artifacts:
  - perf-artifact (ID: 206054130524160, Size: 104889728)
  Fetching signed artifact URL for artifact 206054130524160...
  [Twirp] trace-id: 3eb682d74496336156514e378da205cf
  Signed artifact URL obtained.
  Downloading artifact archive (~100 MB)...
  Artifact download progress: ~100 MB (100% of ~100 MB)
  ::debug::Validating artifact digest for artifact 206054130524160
  Extracting artifact archive to /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4 (~100 MB)...
  Artifact archive extracted to /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4 (~100 MB, 104889728 bytes)
  Artifact 206054130524160 downloaded to /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4 (~100 MB, 104889728 bytes)
  Total of 1 artifact(s) downloaded
  Download artifact has finished successfully

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b756726b-c25e-447c-b671-be1cbd6f80c9.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b756726b-c25e-447c-b671-be1cbd6f80c9.sh
  ls: cannot access 'perf-artifact': No such file or directory
  ::error::Process exited with code 2
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤: 触发含 100MB artifact upload/download 的 workflow
  - 预期结果: 上传/下载均成功且 hash 100% 匹配; 上传<=30s 下载<=30s

- **实际行为**:
  - upload job 成功上传 100MB artifact（multipart 模式）
  - download job 成功下载并解压 artifact archive
  - 但 verify artifact step 执行 `ls -la perf-artifact` 失败：`No such file or directory`
  - 原因: test YAML 中未指定 `download-artifact` 的 `path` 参数，zip 内容解压到了工作目录根下（文件名为原始 `artifact.bin` 而非 `perf-artifact`），而 verify step 期望的是名为 `perf-artifact` 的目录
  - **失败传导链**: download step 成功（二进制正确下载）→ verify step 因文件名不匹配 FAILED → hash_match 断言失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `download` 的 `download artifact step`:
    ```yaml
    - name: download artifact step
      uses: download-artifact
      with:
        name: perf-artifact
    ```
  - **测试 YAML** 中 `download` 的 `verify artifact step`:
    ```yaml
    - name: verify artifact step
      run: |
        ls -la perf-artifact
    ```
  - **GitCode 规格** `writing-pipelines/upload-download-artifacts.md` 第 82-88 行:
    ```yaml
    steps:
      - name: Download artifact
        uses: download-artifact
        with:
          name: app-dist
          path: dist/
    ```
  - **GitCode 规格** `writing-pipelines/upload-download-artifacts.md` 第 92-93 行:
    | `path` | 否 | 下载目标路径，默认为当前工作目录 |
  - **逐项映射**: `uses: download-artifact` → 匹配; `name: perf-artifact` → 匹配; `path` 未指定 → 默认解压到工作目录根（被下载 zip 包含 `artifact.bin`）; verify step 引用 `perf-artifact` → **不匹配**——verify 期望一个名为 `perf-artifact` 的文件/目录，但实际解压后根下文件名为 `artifact.bin`（upload 原始路径）。这是用例中 verify step 与 download step 的 path 预期不一致导致的。

- **环境前置条件验证**: runner 可用，artifact 上传/下载均成功完成；网络带宽正常（~315 MB/s 上传，下载 ~100 MB 完整成功）

**置信度**: 高（`ls: cannot access 'perf-artifact'` 是明确的路径预期不匹配）

**影响**:
- **阻塞性**: 🟢不阻塞 — 上传/下载核心功能正常，仅 verify 步骤断言失败
- **静默性**: 🟢明确报错 — `ls: cannot access` 即时失败
- **影响面**: 🟡同模板 — 影响所有未指定 download-artifact path 且 verify 引用错误文件名的用例
- **综合**: download-artifact 解压行为正确但 verify step 引用路径与实际解压文件名不一致
- **是否有规避手段**: 是（在 download-artifact 中指定 `path: perf-artifact` 或 verify 引用 `artifact.bin`）

**建议**:
- 修复 verify step：将 `ls -la perf-artifact` 改为 `ls -la artifact.bin`，或在 download-artifact 中添加 `path: output/` 并在 verify 中引用 `output/artifact.bin`
- 同模板的所有 artifact 用例应统一检查 download 后 verify 路径
