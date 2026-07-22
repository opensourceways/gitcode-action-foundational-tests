用例 ID:   COMPAT-ARTIFACT-EQUIV-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-049
母意图:    —
标题:      upload/download-artifact 差异——name 唯一性、path 默认、多 artifact 行为与 GitHub 等价性

前置条件:
  - runner 支持 artifact

操作步骤:
  1. 上传多个同名 artifact
  2. 下载 artifact 并验证 path 默认行为
  3. 测试多 artifact 下载

预期结果:
  - 同名 artifact 应按文档规则处理（覆盖或报错）
  - path 默认行为应与 GitHub 一致

验证点:
  - [正向] artifact 上传与下载成功
  - [nonfunctional] 同名冲突处理与文档一致

清理:      重置 fixture 仓库
