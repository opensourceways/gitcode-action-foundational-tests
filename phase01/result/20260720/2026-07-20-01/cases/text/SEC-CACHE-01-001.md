用例 ID:   SEC-CACHE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
母意图:    —
标题:      fork PR 不应能写入或污染主分支的依赖缓存

前置条件:
  - 仓库支持 cache action
  - 主分支 workflow 使用 cache 缓存依赖
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在主分支 push 触发 workflow，使用 `uses: cache` 写入一个已知 key 的缓存（如 key=deploy-deps-001）
  2. 从 fork 仓库提交 PR，在 fork PR 的 workflow 中使用同样的 cache key 写入被污染的内容（如替换 package.json 后重新缓存）
  3. fork PR workflow 完成后，在主分支再次 push 触发 workflow，读取同 key 缓存
  4. 检查主分支 workflow 恢复的缓存内容是否与 fork PR 写入的一致（是否命中 fork 的缓存）
  5. 验证 cache hit/miss 日志

预期结果:
  - 主分支 workflow 读取同 key 缓存时，不应命中 fork PR 写入的缓存条目（cache miss）
  - 主分支原有缓存不被 fork PR 覆盖
  - fork PR 的缓存写入与主分支缓存作用域隔离
  - cache restore 日志显示主分支的缓存命中来自主分支作用域，非 fork PR 作用域

验证点:
  - [负向] 主分支 push workflow 不应命中 fork PR 写入的缓存
  - [负向] fork PR 不应能覆盖主分支已存在的缓存条目
  - [负向] 主分支恢复的缓存内容不应包含 fork PR 注入的修改
  - [正向] 同分支两次 push 之间缓存正确命中（正常缓存行为）

清理:      fixture
