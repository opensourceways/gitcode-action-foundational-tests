用例 ID:   COMPAT-UNIQ-FN-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-013
标题:      substring/replace GitCode 独有函数：验证语义边界与迁移锁定风险

前置条件:
  - 使用标准 fixture 仓库，触发 push 事件获取 atomgit 上下文值

操作步骤:
  1. 使用 substring(atomgit.sha, 0, 7) 截取短 SHA
  2. 测试边界：start 超出长度、start 为负、len 为 0
  3. 使用 replace(atomgit.ref, 'refs/heads/', '') 提取分支名
  4. 测试 replace 是否全局替换、old 不存在时的行为

预期结果:
  - substring 正常返回 7 字符短 SHA
  - start 越界应返回空字符串或明确报错
  - replace 应全局替换所有匹配（非首次替换）
  - 文档应标注「GitCode 独有函数，搬回 GitHub 需用 shell 替代」

验证点:
  - [正向] substring(sha, 0, 7) 返回 7 字符短 SHA
  - [正向] substring 越界行为明确（不应导致 workflow 崩溃）
  - [正向] replace 分支前缀正确
  - [正向] 文档标注 GitCode 独有（迁移锁定风险）

清理:      fixture
