用例 ID:   COMP-ARTIFACT-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-006
标题:      验证 artifact 跨 job 上传/下载及保留策略

前置条件:
  - jobA 使用 upload-artifact 上传文件

操作步骤:
  1. jobA: upload-artifact(name=A, path=dist/) 上传
  2. jobB: download-artifact(name=A) 下载并对比内容
  3. 同 workflow 同名 artifact 重复上传 → 验证行为
  4. 不指定 name 下载全部 artifact
  5. 引用不存在的 artifact → 验证报错

预期结果:
  - 上传→下载文件内容逐字节一致
  - 多路径上传全部包含
  - 不存在的 artifact 报错

验证点:
  - [正向] 上传下载内容一致
  - [正向] 目录结构保留
  - [正向] 多路径文件完整
  - [负向] 不存在的 artifact 报错

清理:      fixture
