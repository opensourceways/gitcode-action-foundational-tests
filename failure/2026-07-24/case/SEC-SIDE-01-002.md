## 失败分诊 · SEC-SIDE-01-002 · Secret 不经 artifact 侧信道绕过脱敏外泄

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, artifact_content) — must_not_contain_secret "DEPLOY_TOKEN"，断言目标 artifact_content 不被引擎支持/artifact 未成功上传；assertions[1] (positive, run_status) — 期望 equals "blocked_or_masked"，实际 run_status=FAILED 且非此复合词汇

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（27 行）:
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
  Step 1（Write secret to file）成功执行（无标准输出，但 script 创建并相应执行）。
  Step 2（Upload artifact）：zip 创建成功（143 bytes），但在调用制品 API 创建 artifact 时被 Twirp 服务拒绝——`Artifact with name already exists: secret-artifact`。制品名 `secret-artifact` 与前次 workflow 运行中残留的制品名冲突，导致上传失败。
  由于 artifact 上传失败，无法检查 secret 是否通过 artifact 侧信道泄漏——测试的完整流程被环境残留阻断。

- **预期行为**（Phase 01 文本用例 `SEC-SIDE-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，将 secret 写入文件并上传为 artifact"
  - 操作步骤 2: "触发 workflow 并下载 artifact 检查内容"
  - 预期结果: "Artifact 中不应包含 secret 明文；若 artifact 包含 secret，应被拦截或遮蔽"
  - 验证点: "[负向] Secret 明文不应以未遮蔽形式出现在上传的 artifact 中"

- **实际行为**:
  - 制品上传因名称冲突（前次运行残留）失败
  - Secret 侧信道泄漏测试完全未被验证——artifact 未成功上传到可下载的资源 ID
  - 断言 target `artifact_content` 依赖 artifact 成功上传后才能读取内容，当前环境下无法验证

- **失败传导链**: Step 1 成功（echo secret 到 secret.txt）→ Step 2 upload-artifact 因名称冲突失败（Artifact with name already exists）→ Job FAILED → artifact 未成功存储 → assertion artifact_content 无法读取 → assertion run_status "blocked_or_masked" FAIL

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `side-artifact` job 的两个步骤:
    ```yaml
    - name: Write secret to file
      run: |
        echo "token=${{ secrets.DEPLOY_TOKEN }}" > secret.txt
    - name: Upload artifact
      uses: upload-artifact
      with:
        name: secret-artifact
        path: secret.txt
    ```
  - 这对应 GitCode 规格 `security-permissions/using-secrets.md` 第 62-69 行的 Secret 安全机制表:
    ```
    | 安全措施 | 说明 |
    |--------|------|
    | 日志遮掩 | Secret 值在日志中自动替换为 *** |
    ```
    规格第 66 行承诺日志遮掩，但未明确 artifact 内容中的 secret 脱敏行为——这是测试意图探索的安全边界。Secret 写入文件后作为 artifact 上传，构成了日志遮掩以外的潜在侧信道泄漏路径。
  - 同时对应 `writing-pipelines/upload-download-artifacts.md` 第 62 行参数表：
    ```
    | name | 是 | 制品名称，同一 workflow 中唯一 |
    ```
    规格第 62 行要求制品名"同一 workflow 中唯一"，但平台实际行为是跨 workflow run 也检查了名称唯一性（`Artifact with name already exists`），这超出了文档承诺的范围，产生了环境残留干扰。

**置信度**: 中（制品名冲突是环境问题已被日志确凿证实；secret 通过 artifact 侧信道泄漏这一安全问题未被实际测试到——测试逻辑被环境残留阻断）

**影响**:
- **阻塞性**: 🟡非阻塞 — workflow 能完成（job FAILED），但 artifact 因名称冲突上传失败，secret 通过 artifact 侧信道泄漏的测试完全未执行到
- **静默性**: 🟡可察觉 — 日志明确提示 `::error::Upload artifact failed: Artifact with name already exists: secret-artifact`，原因可观测
- **影响面**: 🟢单用例 — 仅影响 SEC-SIDE-01-002 的 artifact 侧信道测试，与 artifact 名称跨 run 冲突相关
- **综合**: 制品名 `secret-artifact` 与前次运行残留冲突导致上传失败，secret 侧信道泄漏的安全边界未被实际测试到
- **是否有规避手段**: 是 — 使用带时间戳的唯一制品名称避免跨 run 冲突；在 teardown 中清理前次残留 artifact

**建议**:
- 在 teardown 中清理前次运行残留的 artifact（使用唯一名称后缀如时间戳以避免跨 run 冲突）
- 若 artifact 上传成功，需设计下载并验证 artifact 内容的步骤（当前测试缺少下载验证环节）
- 相关用例: SEC-SIDE-01-001
