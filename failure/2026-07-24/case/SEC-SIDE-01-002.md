## 失败分诊 · SEC-SIDE-01-002 · Secret 不经 artifact 侧信道绕过脱敏外泄

**判定结果**: FAIL
**失败断言**: 
- negative, artifact_content, must_not_contain_secret "DEPLOY_TOKEN" — 无法验证
- positive, run_status, equals "blocked_or_masked" — 实际为 artifact 名称冲突，不匹配

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (27 行):
  ```
  === JOB: Test secret in artifact (status=FAILED) ===
  [2026/07/23 22:10:16.649 GMT+08:00] [INFO] Job(1529973953235795968_1529973953202241543) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4a835b39-71c0-4f31-b405-ec407966ec2c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4a835b39-71c0-4f31-b405-ec407966ec2c.sh
  
  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
  Uploading artifact "secret-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/secret.txt
  ::debug::followSymbolicLinks 'true'
  ::debug::implicitDescendants 'true'
  ::debug::matchDirectories 'true'
  ::debug::omitBrokenSymbolicLinks 'true'
  ::debug::followSymbolicLinks 'true'
  ::debug::implicitDescendants 'true'
  ::debug::matchDirectories 'true'
  ::debug::omitBrokenSymbolicLinks 'true'
  ::debug::Search path '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/secret.txt'
  Found 1 file(s) to upload
  ::debug::[diagnostic] First 1 matched file(s): /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/secret.txt
  ::debug::Resolved root directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
  Creating zip archive from 1 file(s)...
  Zip archive created: /tmp/artifact-1784815831357-b9936438.zip (~0 MB, 143 bytes)
  Creating artifact "secret-artifact" (size: 143 bytes, workflow: 92877ce27bff4e149e2f5985f84e9b19)...
  [Twirp] trace-id: ad7d66b86ee5ad36e2572cdfc8d00b56
  [Twirp] error trace-id: ad7d66b86ee5ad36e2572cdfc8d00b56
  ::debug::Temp zip file removed: /tmp/artifact-1784815831357-b9936438.zip
  ::error::Upload artifact failed: Artifact with name already exists: secret-artifact, repoId=10431328, workflowId=92877ce27bff4e149e2f5985f84e9b19
  ```

- **预期行为** (Phase 01 文本用例 SEC-SIDE-01-002, 优先级 P0, 维度 security):
  - 前置条件: 仓库配置了 secret `DEPLOY_TOKEN`
  - 操作步骤 1: 提交一个 workflow，将 secret 写入文件并上传为 artifact
  - 操作步骤 2: 触发 workflow 并下载 artifact 检查内容
  - 预期结果: Artifact 中不应包含 secret 明文；若 artifact 包含 secret，应被拦截或遮蔽

- **实际行为**:
  - Step 1 (`echo "token=..." > secret.txt`): 成功创建文件（143 bytes zip 确认文件有内容）
  - Step 2 (upload-artifact): **上传失败** — 原因: `Artifact with name already exists: secret-artifact`
  - 同一 workflow 的前一次运行或并行运行已使用该名称上传了 artifact
  - 无法验证 artifact 内容是否被遮蔽/拦截（上传步骤失败）

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 66 行: "日志遮掩 | Secret 值在日志中自动替换为 `***`"
  - 第 119 行: "不要把 secret 写入制品或缓存"（安全建议）

- **环境前置条件验证**: YAML `setup.secrets: ["DEPLOY_TOKEN"]`。无 config_probe。artifact 名称 `secret-artifact` 存在冲突，可能来自前次测试运行未清理。

**置信度**: 高 (artifact 名称冲突导致上传失败，非功能缺陷)

**影响**:
- **阻塞性**: 🔴阻塞 — artifact 侧信道泄露验证完全无法执行
- **静默性**: 🟢明确报错 — "Artifact with name already exists" 明确指示冲突
- **影响面**: 🟢单用例 — 仅此用例因 artifact 名称冲突失败
- **综合**: 前次测试遗留的 artifact 名称冲突导致上传失败；需在 teardown 中清理或使用唯一名称
- **是否有规避手段**: 是

**建议**:
- 测试 YAML 中为 artifact 名称添加随机后缀或时间戳避免冲突：`name: "secret-artifact-${{ atomgit.run_id }}"`
- 在 setup/teardown 阶段清理残留 artifact
- 添加 config_probe 确认 `DEPLOY_TOKEN` secret 存在且有效
- 在上传成功后增加下载步骤验证内容是否被遮蔽
