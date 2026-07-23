用例 ID:   COMPAT-PRE-MERGE-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-051
标题:      checkout 插件的 PR 预合并（pre-merge）行为——历史 #25/#71

前置条件:
  - 创建 PR：源分支修改文件 A，目标分支修改同一文件 A 产生冲突
  - 配置 pull_request 触发 workflow 含 checkout

操作步骤:
  1. 在目标分支修改文件 conflict.txt 为内容 "base"
  2. 在源分支修改同一文件为内容 "head"（与 base 冲突）
  3. 创建 PR，触发 pull_request workflow
  4. 观察 checkout 结果：是 merge commit 还是源分支 head

预期结果:
  - GitHub 行为：checkout 预合并结果（merge commit），检测到冲突时有临时合并产物
  - GitCode 行为：可能 checkout 源分支 head commit，不执行预合并
  - 此为核心行为差异，文档需明确声明

验证点:
  - [正向] checkout 结果可观测（检查 conflict.txt 内容或 GIT_SHA）
  - [正向] 文档声明是否支持 pre-merge checkout
  - [负向] 不应 checkout 失败且无日志说明原因

清理:      fixture
