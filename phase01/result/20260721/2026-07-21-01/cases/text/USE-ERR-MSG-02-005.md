用例 ID:   USE-ERR-MSG-02-005
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-003
标题:      未知字段/不支持属性时的错误信息可诊断性

前置条件:
  - 在 YAML 中添加 GitCode 不支持的 GitHub 字段
  - container.credentials / services 等

操作步骤:
  1. 添加 `jobs.<id>.container.credentials`（GitHub 有但 GitCode 不支持）
  2. 添加 `jobs.<id>.services`（GitHub 有但 GitCode 不支持）
  3. 观察是报错还是静默忽略
  4. 若报错：消息是否指明字段路径 + 该字段 GitCode 不支持
  5. 若忽略：是否有 warning 级别日志

预期结果:
  - 不支持字段应报错（非静默忽略）
  - 若忽略则必有 warning 日志
  - 消息含字段路径 + GitCode 不支持提示

验证点:
  - [正向] 不支持字段有可见提示（错误/警告）
  - [正向] 消息指明字段路径
  - [负向] 不应完全静默忽略

可理解性判据: eval: llm_assisted
清理:      fixture
