用例 ID:   COMPAT-ARTIFACT-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-026
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    COMPAT-ARTIFACT-01-001
标题:      upload-artifact 保留期行为等价性

前置条件:
  - 仓库已启用 upload-artifact 插件

操作步骤:
  1. 在工作流中使用 `uses: upload-artifact` 上传文件
  2. 配置保留期参数（如 retention-days）
  3. 观察 artifact 在系统中的保留与过期行为

预期结果:
  - upload-artifact 支持保留期参数配置
  - 超过保留期后 artifact 被自动清理
  - 保留期内 artifact 可正常下载
  - 裸插件名写法与 GitHub 全名写法在保留期语义上等价

验证点:
  - [正向] 保留期内可正常下载 artifact
  - [正向] 超过保留期后 artifact 被清理或不可访问
  - [负向] 不应出现保留期配置被静默忽略的情况

清理:      fixture
