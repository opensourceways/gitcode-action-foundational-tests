用例 ID:   COMPAT-OUTPUT-LIMIT-02-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-046
母意图:    —
标题:      step 输出/artifact 超限行为差异——1MB output、artifact 上限的降级方式

前置条件:
  - workflow 产生超过 1MB 的 step 输出与 artifact

操作步骤:
  1. 在 step 中输出超过 1MB 的文本
  2. 上传超过上限的 artifact
  3. 观察截断/报错行为

预期结果:
  - 超限输出应被截断或报错
  - artifact 超限应给出明确的降级提示

验证点:
  - [正向] 超限后 workflow 不崩溃
  - [nonfunctional] 降级方式与文档一致

清理:      重置 fixture 仓库
