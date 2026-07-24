## 失败分诊 · REL-ARTPERF-01-053 · 制品传输性能——100MB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 upload/download 均 success，实际 download job status=FAILED；assertions[1] (positive, run_logs) — 期望下载后 hash 匹配，实际 verify 步骤报错 `ls: cannot access 'perf-artifact': No such file or directory`

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（仅 81 行）:
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
  Artifact "perf-artifact" finalized successfully.
  ...
  Artifact "perf-artifact" uploaded successfully. ID: 206054130524160, Size: 104889728 bytes
  Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-4/actions/artifacts/206054130524160

  === JOB: download artifact job (status=FAILED) ===
  [2026/07/23 22:25:36.143 GMT+08:00] [INFO] Job(1529977724519452672_1529977724494286857) duration check: true
  ...
  Downloading single artifact
  ::debug::Found named artifact 'perf-artifact' (ID: 206054130524160, Size: 104889728)
  ...
  Artifact download progress: ~100 MB (100% of ~100 MB)
  ...
  Artifact 206054130524160 downloaded to /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4 (~100 MB, 104889728 bytes)
  Total of 1 artifact(s) downloaded
  Download artifact has finished successfully

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b756726b-c25e-447c-b671-be1cbd6f80c9.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b756726b-c25e-447c-b671-be1cbd6f80c9.sh
  ls: cannot access 'perf-artifact': No such file or directory
  ::error::Process exited with code 2
  ```
  日志显示：upload job 完全成功——100MB 文件上传到 ID 206054130524160。download job 的 artifact 下载步骤也完全成功——`~100 MB downloaded`、`Download artifact has finished successfully`。但在后续的 shell verify 步骤中，`ls: cannot access 'perf-artifact'`——artifact 下载后被解压到工作目录，但脚本期望的文件名 `perf-artifact`（artifact name）与实际解压出的文件名 `artifact.bin`（原始文件名）不匹配。这是 artifact 提取路径语义问题（下载的 artifact 保留了原始文件名 `artifact.bin`，而非 artifact 名称 `perf-artifact`）。

- **预期行为**（Phase 01 文本用例 `REL-ARTPERF-01-053`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 100MB artifact upload/download 的 workflow"
  - 预期结果: "上传/下载均成功且 hash 100% 匹配；上传≤30s 下载≤30s"
  - 验证点: "[正向] 上传≤30s；[正向] 下载≤30s；[正向] hash 100% 匹配"

- **实际行为**:
  - upload 成功，约 0.3s（远低于 30s 限制）
  - download 也成功（约 20s），但 verify 脚本用了 artifact 名称 `perf-artifact` 查找文件，实际解压出的文件名为 `artifact.bin`，导致 ls 找不到文件报 exit code 2
  - hash 校验未执行

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `download artifact job` 的 verify step: 执行 `ls perf-artifact` 期望验证下载的文件存在
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/upload-download-artifacts.md` 的 download-artifact 行为。规格描述 artifact 被下载和解压到工作目录——但解压后的文件名取决于上传时的原始路径名（`artifact.bin`），而非 artifact 名称（`perf-artifact`）。测试脚本假设了 artifact name = 文件名，这导致路径不匹配。

**置信度**: 中（下载步骤本身成功，但 verify 脚本中文件路径预期与 artifact 解压后实际路径不匹配，属于测试脚本编写问题而非平台缺陷）

**建议**:
- 修复测试脚本的 verify 步骤——使用正确的解压后文件名 `artifact.bin` 或使用通配符 `ls` 检查所有解压文件
- 相关用例: REL-ART-01-041
