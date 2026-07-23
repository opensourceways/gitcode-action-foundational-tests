用例 ID:   COMP-ARTIFACT-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-006
母意图:    —
标题:      验证 artifact 跨 job 上传/下载及保留策略

前置条件:  仓库支持 artifact 上传/下载

操作步骤:
  1. job A 上传 artifact（name=test-artifact, path=dist/）
  2. job B（needs [A]）下载同名 artifact
  3. 比对上传和下载文件的 SHA256 一致性
  4. 测试同名 artifact 重复上传行为
  5. 测试下载不存在的 artifact 的报错

预期结果:
  - 上传→下载→文件内容逐字节一致
  - 目录结构与 glob 模式上传正确
  - 同名 artifact 重复上传有明确行为
  - 下载不存在的 artifact 报错

验证点:
  - [正向] 文件内容逐字节一致
  - [正向] 多路径上传全部包含
  - [负向] 下载不存在的 name 报错
  - [非功能] artifact 保留期后可确认不可下载

清理:      fixture
