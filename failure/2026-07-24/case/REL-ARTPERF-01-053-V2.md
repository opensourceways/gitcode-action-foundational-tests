## 失败分诊 · REL-ARTPERF-01-053-V2 · 制品传输性能——1GB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: 非功能/upload_time_seconds ≤300 actual=upload未成功; 非功能/download_time_seconds ≤300 actual=N/A; 正向/hash_match expected=true actual=N/A

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（57 行）:
  ```
  === JOB: upload artifact job (status=FAILED) ===
  [2026/07/23 22:26:17.443] [INFO] Job(1529977983043514368_1529977983022542849) duration check: true
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
  Zip archive progress tracking enabled (~1024 MB source data)
  Zip archive created: /tmp/artifact-1784816791200-c57f61a7.zip (~1024 MB, 1074069497 bytes)
  Creating artifact "perf-artifact" (size: 1074069497 bytes, workflow: 5e6d6460f31a4672953d5d33acae7f20)...
  [Twirp] trace-id: edcc59d4825606e402c9ed597975481a
  Artifact created with ID 206054481891328, upload mode: multipart
  Uploading artifact via multipart (partSize: 209715200 bytes, totalParts: 6)...
  Artifact multipart upload started (~1024 MB archive, 6 part(s))
  Starting upload with concurrency: 6
  ::debug::Multipart upload: sending part 1/6 (~200 MB)...
  ::debug::Multipart upload: sending part 2/6 (~200 MB)...
  ::debug::Multipart upload: sending part 3/6 (~200 MB)...
  ::debug::Multipart upload: sending part 4/6 (~200 MB)...
  ::debug::Multipart upload: sending part 5/6 (~200 MB)...
  ::debug::Multipart upload: sending part 6/6 (~24 MB)...
  Artifact multipart upload progress: ~1024 MB (100% of ~1024 MB)
  ::debug::Multipart upload: part 6/6 done, etag=39dfb4812ddd90951c89c53de8a410b8, size=25493497
  ::debug::Multipart upload: part 5/6 done, etag=9152c8aa5e249c23c4b944f01d2efd4c, size=209715200
  ::debug::Multipart upload: part 1/6 done, etag=0cd00248c548126bce6cf41644c27f0b, size=209715200
  ::debug::Multipart upload: part 4/6 done, etag=054b959e91ec97600819356117521ec4, size=209715200
  ::debug::Multipart upload: part 2/6 done, etag=d7e40b57565980ab70a0dee0b377e7c4, size=209715200
  ::debug::Multipart upload: part 3/6 done, etag=3eb53e1af1a22cf5b73c6ec8b342520a, size=209715200
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

- **预期行为**（Phase 01 文本用例 REL-ARTPERF-01-053-V2，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤 1: 触发含 1GB artifact upload/download 的 workflow
  - 预期结果: 上传/下载均成功且 hash 100% 匹配; 上传≤300s 下载≤300s

- **实际行为**:
  - 1GB 文件成功生成，zip 打包成功，6 个分片全部成功上传到存储
  - 但在 Finalizing 阶段，平台拒绝：`Namespace artifact quota exceeded`
  - 当前已使用 1,506,363,281 bytes (~1.4 GB)，请求新增 1,074,069,497 bytes (~1 GB)，超出 namespace 配额上限 1,073,741,824 bytes (1 GB)
  - 此前已有其他 artifact 占用配额，导致本用例上传被拒

- **对照 GitCode 规格**:
  - 无直接相关规格段落；平台 artifact 存储有 1 GB namespace 配额限制

- **环境前置条件验证**: runner 可用、文件生成和分片上传均正常完成，配额在 finalizing 阶段检查

**置信度**: 高 (平台明确返回配额超限错误，所有 6 个分片上传成功说明网络和存储通道正常)

**影响**:
- **阻塞性**: 🔴阻塞 — 需要清理 namespace artifact 配额后才能重新测试
- **静默性**: 🟢明确报错 — `Namespace artifact quota exceeded` 明确提示
- **影响面**: 🟡同维度 — 影响同一 namespace 下的 artifact 压力测试
- **综合**: 平台 artifact 存储配额为 1 GB/namespace，本用例 1 GB 文件叠加已有 artifact 导致超额
- **是否有规避手段**: 是（清理 namespace 中已有 artifact，或提升配额）

**建议**:
- Phase 02 在测试前清理目标 namespace 的历史 artifact
- 平台方考虑是否提升 artifact 配额或提供 quota reset API
