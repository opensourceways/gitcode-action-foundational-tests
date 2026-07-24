## 失败分诊 · SEC-SIDE-01-002 · Secret 不经 artifact 侧信道绕过脱敏外泄

**判定结果**: FAIL
**失败断言**:
  - 负向 `artifact_content` `must_not_contain_secret: "DEPLOY_TOKEN"` — 无法验证: artifact 上传失败
  - 正向 `run_status` `equals: "blocked_or_masked"` — **FAIL**: artifact 上传失败因 "名称已存在" 而非因包含 secret

**根因初判**: 测试 YAML 的 artifact name 冲突（`secret-artifact` 已存在），非秘密泄露问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
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

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了 secret DEPLOY_TOKEN
  - 操作步骤: 1. 将 secret 写入文件并上传为 artifact；2. 下载 artifact 检查内容
  - 预期结果: Artifact 中不应包含 secret 明文

- **实际行为**:
  - 文件创建成功（secret.txt, 143 bytes 压缩后）
  - artifact 上传失败: `Artifact with name already exists: secret-artifact`
  - 该流水线（workflowId=92877ce27bff...）中已存在同名 artifact，拒绝重复创建
  - 测试未达到下载 artifact 检查内容阶段
  - **失败传导链**: 上次 test run 残留同名 artifact → Twirp 服务拒绝重复 → 上传失败 → 无法下载检查内容

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `side-artifact` 的 `Write secret to file` 和 `Upload artifact`:
    ```yaml
    setup:
      secrets: ["DEPLOY_TOKEN"]
    jobs:
      side-artifact:
        name: Test secret in artifact
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Write secret to file
            run: |
              echo "token=${{ secrets.DEPLOY_TOKEN }}" > secret.txt
          - name: Upload artifact
            uses: upload-artifact
            with:
              name: secret-artifact
              path: secret.txt
    ```
  - **GitCode 规格** `core-concepts/artifacts-and-cache.md` 第 7-19 行:
    ```yaml
    steps:
      - uses: upload-artifact
        with:
          name: build-output
          path: dist/
    ```
  - **逐项映射**:
    - `name: secret-artifact`: 测试 YAML 使用固定名称 — 与规格示例结构一致
    - `path: secret.txt`: 包含 secret 的文件 — 这是注入风险点
    - 规格未说明 artifact name 的唯一性约束（per workflow 唯一 vs 全局唯一）

- **环境前置条件验证**: 上次 test run 的 artifact 残留导致名称冲突

**置信度**: 高（artifact name 冲突，与 secret 泄露验证无关）

**影响**:
- **阻塞性**: 中 — artifact 名称冲突阻止了核心验证
- **静默性**: 低 — 平台明确报出名称冲突错误
- **影响面**: 低 — 可通过清理 artifact 或使用动态名称解决
- **综合**: artifact 上传因名称冲突（`secret-artifact` 已存在于同一 workflow）失败，测试未达到 secret 侧信道泄露的验证阶段
- **是否有规避手段**: 是 — 在测试 setup 中清理残留 artifact；或使用带时间戳的动态名称

**建议**:
- Phase 02: (1) 测试 setup 阶段先调用 artifact 删除 API 清理残留；(2) 或使用 `${atomgit.run_id}` 生成唯一 artifact 名称
- Phase 01: 增加 teardown 步骤清理测试 artifact
