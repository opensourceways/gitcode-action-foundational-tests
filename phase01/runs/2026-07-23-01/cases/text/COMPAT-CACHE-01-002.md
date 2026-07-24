用例 ID:   COMPAT-CACHE-01-002
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-025
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    COMPAT-CACHE-01-001
标题:      cache 行为等价性——fork PR 写隔离

前置条件:
  - 仓库已启用 cache 插件
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 fork PR 的工作流中使用 `uses: cache` 尝试写入新缓存
  2. 观察 fork PR 场景下的缓存写入行为
  3. 对比同一缓存 key 在主干分支上的写入权限

预期结果:
  - fork PR 不应覆盖或污染主干分支的缓存条目
  - fork PR 可读取公共缓存，但写入应被隔离或拒绝
  - 系统应为 fork 提供独立的缓存命名空间或阻止写入

验证点:
  - [负向] fork PR 不应成功覆盖主干缓存
  - [正向] 主干缓存保持完整未被污染
  - [正向] 系统提供明确的缓存隔离机制

清理:      fixture
