用例 ID:   COMP-ARTIFACT-01-001
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-015
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      artifact 可在同 workflow 的 job 间正确传递

前置条件:
  - workflow 含 upload-artifact 和 download-artifact

操作步骤:
  1. job 1 生成文件并 upload-artifact
  2. job 2 通过 needs 依赖下载 artifact
  3. 验证文件内容一致性

预期结果:
  - job 2 下载的 artifact 内容与 job 1 上传的一致

验证点:
  - [正向] download 后文件内容正确
  - [正向] 运行状态成功

清理:      none
