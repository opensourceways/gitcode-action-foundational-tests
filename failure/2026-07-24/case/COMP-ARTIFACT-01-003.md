## 失败分诊 · COMP-ARTIFACT-01-003 · artifact 保留期设置生效

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, artifact_available) — 期望 `yes_within_retention`，实际 `FAILED`（平台缺陷导致 job 执行失败）
assertions[1] (positive, artifact_available_after_expiry) — 期望 `no_after_1_day`，下游随上游失败而 IGNORED

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（共 2 行）:
```
=== JOB: Upload with short retention (status=FAILED) ===
[2026/07/23 22:11:53.181 GMT+08:00] [INFO] Job(1529974358023880704_1529974357990326279) duration check: true
```

  **日志分析**: Job "Upload with short retention" status=FAILED, 0 字节有效日志，制品上传流程完全无 shell 输出

- **预期行为**（Phase 01 文本用例 `COMP-ARTIFACT-01-003`，优先级 P1，维度 completeness）:
  - 操作步骤 1: "上传 artifact 并设置 retention-days: 1"
  - 操作步骤 2: "等待超过保留期后尝试下载"

  预期结果:
  - 超过保留期后 artifact 不可下载

  验证点:
  - [正向] 保留期内可下载 artifact
  - [负向] 超过保留期后下载返回 404

- **实际行为**:
  - Job "Upload with short retention" status=FAILED, 0 字节有效日志，制品上传流程完全无 shell 输出


- **测试 YAML 与规格精确对照**:
  - 规格文件: `upload-download-artifacts.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/upload-download-artifacts.md`)
  - 规格节选:
```yaml
steps:
  - uses: upload-artifact
    with:
      name: app-dist
      path: dist/
```
    该规格明确声明: 15-18行的上传制品示例，使用了 `uses: upload-artifact` 裸插件名

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（Job "Upload with short retention" status=FAILED, 0 字节有效日志，制品上传流程完全无 shell 输出）

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-ARTIFACT-01-003.log`
- 建议修复后重新验跑 COMP-ARTIFACT-01-003
- 相关用例: COMP-ARTIFACT-01-002
