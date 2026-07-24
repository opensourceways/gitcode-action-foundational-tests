## 失败分诊 · REL-ARTPERF-01-053-V2 · 制品传输性能——1GB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: 非功能/upload_time_seconds le=300 actual=N/A; 非功能/download_time_seconds le=300 actual=N/A; 正向/hash_match expected=true actual=N/A

**根因初判**: 平台缺陷（artifact namespace quota 超限）
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: upload artifact job (status=FAILED) ===
  [2026/07/23 22:26:17.443 GMT+08:00] [INFO] Job(1529977983043514368_1529977983022542849) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/03691558-0708-4330-86d3-fe0d74079a91.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/03691558-0708-4330-86d3-fe0d74079a91.sh
  1024+0 records in
  1024+0 records out
  1073741824 bytes (1.1 GB, 1.0 GiB) copied, 2.43541 s, 441 MB/s

  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  Uploading artifact "perf-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/artifact.bin
  ...
  Creating zip archive from 1 file(s)...
  Zip archive created: /tmp/artifact-1784816791200-c57f61a7.zip (~1024 MB, 1074069497 bytes)
  Creating artifact "perf-artifact" (size: 1074069497 bytes, workflow: 5e6d6460f31a4672953d5d33acae7f20)...
  [Twirp] trace-id: edcc59d4825606e402c9ed597975481a
  Artifact created with ID 206054481891328, upload mode: multipart
  Uploading artifact via multipart (partSize: 209715200 bytes, totalParts: 6)...
  Artifact multipart upload started (~1024 MB archive, 6 part(s))
  Starting upload with concurrency: 6
  ...
  All parts uploaded. Completing multipart upload...
  [Twirp] trace-id: 3944e734b230fcfc75821b7e92006b30
  Upload complete. SHA-256: 281e89c5d03080506adc6b08dabbf26f1294c0798b4d8ae495b735279263c1ce
  Finalizing artifact...
  [Twirp] trace-id: 22d3fd4e0e48c67ea4e6143081c27a92
  [Twirp] error trace-id: 22d3fd4e0e48c67ea4e6143081c27a92
  ::warning::Upload failed, artifact ID 206054481891328 may require cleanup on the server.
  ::debug::Temp zip file removed: /tmp/artifact-1784816791200-c57f61a7.zip
  ::error::Upload artifact failed: Namespace artifact quota exceeded: namespace=13965860, repoId=10431319, requestedBytes=1074069497, currentUsed=1506363281, max=1073741824

  === JOB: download artifact job (status=IGNORED) ===
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤: 触发含 1GB artifact upload/download 的 workflow
  - 预期结果: 上传/下载均成功且 hash 100% 匹配; 上传<=300s 下载<=300s

- **实际行为**:
  - 1GB 文件成功生成（441 MB/s），zip 创建成功，所有 6 个 multipart 分片成功上传
  - 但在 `Finalizing artifact` 阶段，平台返回 `Namespace artifact quota exceeded`
  - namsepace 当前已用 ~1.5GB，超过 1GB max（quota 限制），请求的 1GB artifact 无法保存
  - download job 因 upload 失败被 IGNORED
  - **失败传导链**: upload 分片全部上传成功 → finalize 时 quota 检查失败 → upload FAILED → download IGNORED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `upload` 的 steps:
    ```yaml
    - name: generate 1024MB file
      run: |
        dd if=/dev/urandom of=artifact.bin bs=1M count=1024
    - name: upload artifact step
      uses: upload-artifact
      with:
        name: perf-artifact
        path: artifact.bin
    ```
  - **GitCode 规格** `writing-pipelines/upload-download-artifacts.md` 第 51-58 行:
    ```yaml
    steps:
      - name: Upload artifact
        uses: upload-artifact
        with:
          name: app-dist
          path: dist/
    ```
  - **GitCode 规格** `core-concepts/artifacts-and-cache.md` 第 12-18 行:
    ```yaml
    steps:
      - uses: upload-artifact
        with:
          name: build-output
          path: dist/
    ```
  - **逐项映射**: `uses: upload-artifact` → 匹配; `name: perf-artifact` → 匹配; `path: artifact.bin` → 匹配; `dd bs=1M count=1024` 生成 1GB 文件 → 规格未限制 artifact 大小上限。测试 YAML 写法与规格一致，触发的是平台 quota 限制而非 YAML 错误。

- **环境前置条件验证**: runner 可用（1GB 文件成功生成），multipart upload 全部成功，网络带宽正常；平台 artifact quota 为 namespace 级别限制（max=1GB）

**置信度**: 高（`Namespace artifact quota exceeded` 是明确的平台配额拒绝，根因直指平台限制）

**影响**:
- **阻塞性**: 🔴阻塞 — namespace quota 限制 1GB，任何超过 1GB 的 artifact 用例无法执行
- **静默性**: 🟢明确报错 — `Namespace artifact quota exceeded` 清晰提示
- **影响面**: 🟡同 namespace — 影响所有大 artifact 用例（共享同一 namespace quota）
- **综合**: 平台 artifact namespace 配额仅为 1GB，1GB 单项 artifact 即超限
- **是否有规避手段**: 是（先清理历史 artifact 释放 namespace quota，或申请提高配额）

**建议**:
- 平台方需评估 namespace artifact quota 是否应为动态累计或应有更大上限
- 测试前需确保 namespace quota 未超限（已有 1.5GB 占用），清理历史 artifact
- 同 namespace 的 artifact 用例应顺序执行并清理，避免累计超 quota
