用例 ID:   SEC-CACHE-ISOLATE-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-020
母意图:    —
标题:      cache key 跨项目/跨仓库作用域隔离（无横向污染）

前置条件:
  - 存在两个独立仓库 repo-A 与 repo-B
  - 两仓库均配置了同名 cache key

操作步骤:
  1. 在 repo-A 的 workflow 中写入 cache（key=shared-test-key）
  2. 在 repo-B 的 workflow 中尝试 restore 相同 key
  3. 观察 repo-B 的 cache 命中状态

预期结果:
  - repo-B 应产生 CACHE_MISS，不应读取到 repo-A 的缓存数据
  - 缓存作用域应至少隔离到仓库级别

验证点:
  - [负向] 日志不含 repo-A 写入的缓存内容
  - [正向] repo-B 出现 CACHE_MISS

清理:      重置 fixture 仓库
