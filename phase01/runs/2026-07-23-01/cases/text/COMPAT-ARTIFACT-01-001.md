用例 ID:   COMPAT-ARTIFACT-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-026
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      upload/download-artifact 跨 job 传递等价性

前置条件:
  - 仓库已启用 upload-artifact 与 download-artifact 插件

操作步骤:
  1. 在 job A 中使用 `uses: upload-artifact` 上传一个标记文件
  2. 在 job B 中使用 `uses: download-artifact` 下载同一文件
  3. 验证 job B 能正确读取到 job A 上传的文件内容

预期结果:
  - upload-artifact 成功上传文件到 artifact 存储
  - download-artifact 成功下载并恢复文件到 job B 工作目录
  - 文件内容在跨 job 传递后保持一致
  - 裸插件名写法行为与 GitHub 全名写法等价

验证点:
  - [正向] upload-artifact 步骤成功，无报错
  - [正向] download-artifact 步骤成功，无报错
  - [正向] job B 中文件内容与 job A 上传时一致
  - [负向] 不应因使用裸插件名而解析失败

清理:      fixture
