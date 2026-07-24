## 失败分诊 · REL-ARTPERF-01-053 · 制品传输性能——100MB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: 正向/hash_match expected=true actual=N/A; 非功能/upload_time_seconds ≤30 actual=N/A; 非功能/download_time_seconds ≤30 actual=N/A

**根因初判**: 用例问题
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（81 行）:
  ```
  === JOB: upload artifact job (status=COMPLETED) ===
  [2026/07/23 22:25:15.777] [INFO] Job(1529977724519452672_1529977724494286855) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c5c59c65-3e0e-47f1-88b4-5ee920e9f8fb.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c5c59c65-3e0e-47f1-88b4-5ee920e9f8fb.sh
  100+0 records in
  100+0 records out
  104857600 bytes (105 MB, 100 MiB) copied, 0.332445 s, 315 MB/s
  
  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Uploading artifact "perf-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ...
  Creating zip archive from 1 file(s)...
  Zip archive progress tracking enabled (~100 MB source data)
  Zip archive created: /tmp/artifact-1784816729497-69002377.zip (~100 MB, 104889728 bytes)
  Creating artifact "perf-artifact" (size: 104889728 bytes, workflow: 37377f8b2720406ca6780f11c1fe26ed)...
  ...
  Artifact "perf-artifact" finalized successfully.
  Artifact "perf-artifact" uploaded successfully. ID: 206054130524160, Size: 104889728 bytes

  === JOB: download artifact job (status=FAILED) ===
  [2026/07/23 22:25:36.143] [INFO] Job(1529977724519452672_1529977724494286857) duration check: true
  ...
  Downloading single artifact
  ::debug::Found 1 artifact(s)
  ::debug::Found named artifact 'perf-artifact' (ID: 206054130524160, Size: 104889728)
  ...
  Downloading artifact archive (~100 MB)...
  Artifact download progress: ~100 MB (100% of ~100 MB)
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

- **预期行为**（Phase 01 文本用例 REL-ARTPERF-01-053，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤 1: 触发含 100MB artifact upload/download 的 workflow
  - 预期结果: 上传/下载均成功且 hash 100% 匹配; 上传≤30s 下载≤30s

- **实际行为**:
  - upload job 成功完成，artifact 上传并 finalized
  - download job 成功下载并解压 artifact（100MB 完整下载）
  - 但 verify step 执行 `ls -la perf-artifact` 失败：下载解压出的文件名为 `artifact.bin`（上传时的原始文件名），而非 artifact 名称 `perf-artifact`
  - download job 最终状态 FAILED，原因仅是 verify step 的文件路径错误

- **对照 GitCode 规格**:
  - 无直接相关规格段落；artifact 下载后解压的文件保持原始名称，验证脚本应使用正确的文件路径

- **环境前置条件验证**: upload/download artifact 基础设施正常（上传 22:25:15 → 下载 22:25:36，均在合理时间内）

**置信度**: 高 (verify step 的 `ls -la perf-artifact` 命令明显与下载解压后的实际文件名 `artifact.bin` 不匹配)

**影响**:
- **阻塞性**: 🟡非阻塞 — 核心 artifact 上传下载功能正常，仅验证脚本路径错误
- **静默性**: 🟢明确报错 — `ls: cannot access 'perf-artifact': No such file or directory`
- **影响面**: 🟢单用例 — 仅限本用例的 verify step
- **综合**: artifact 上传下载流程完整正常，但 verify step 使用了错误的文件路径导致误报失败
- **是否有规避手段**: 是（修正 verify step 为 `ls -la artifact.bin` 或检查解压目录内容）

**建议**:
- Phase 01 修正文本用例的验证步骤，明确下载后文件名与 upload 原始文件名一致
- Phase 02 YAML 中 verify step 改为检查正确的文件名（`artifact.bin`）
