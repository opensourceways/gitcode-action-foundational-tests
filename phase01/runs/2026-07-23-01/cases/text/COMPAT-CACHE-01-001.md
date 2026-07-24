用例 ID:   COMPAT-CACHE-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-025
参照来源:  inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
母意图:    —
标题:      cache 行为等价性——缓存命中场景

前置条件:
  - 仓库已启用 cache 插件
  - 首次运行已生成缓存条目

操作步骤:
  1. 在工作流中使用 `uses: cache` 配置 key 和 path
  2. 首次运行生成缓存后，再次触发同一工作流
  3. 观察第二次运行的缓存恢复行为

预期结果:
  - 第二次运行时 cache 步骤识别到已有缓存并命中
  - 命中后无需重新生成，直接恢复缓存目录内容
  - cache 插件裸名写法行为与 GitHub 全名写法等价

验证点:
  - [正向] 第二次运行日志中出现缓存命中标识
  - [正向] 缓存目录内容正确恢复
  - [负向] 不应因 key 匹配而实际未恢复内容

清理:      fixture
