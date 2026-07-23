用例 ID:   COMPAT-CACHE-SCP-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-052
标题:      cache 插件跨 job/跨 run 作用域与 key 行为——restore-keys 降级与 fork PR 隔离

前置条件:
  - workflow 含两个 job：第一个写 cache，第二个读 cache
  - 使用 restore-keys 前缀降级匹配

操作步骤:
  1. job-A 使用 cache key=node-deps-linux-${{ hashFiles('package.json') }} 写入缓存
  2. job-B（needs: job-A）使用 restore-keys: node-deps- 恢复缓存
  3. 验证 job-B 是否命中 job-A 写入的 cache
  4. fork PR 场景下测试 cache 写隔离（不应可写主分支 cache）

预期结果:
  - restore-keys 前缀降级匹配生效（命中前缀匹配的最近缓存）
  - fork PR 不应可写主分支 cache（cache 投毒防范）
  - cache-hit 输出正确反映命中状态

验证点:
  - [正向] restore-keys 前缀匹配正确恢复缓存
  - [正向] cache-hit 输出布尔值反映命中状态
  - [负向] fork PR 不应可写入主分支 cache

清理:      fixture
