用例 ID:   COMPAT-PRTYPES-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-007
标题:      pull_request types 命名差异：open/update/merge vs opened/synchronize

前置条件: 仓库配置 pull_request 触发器
操作步骤:
  1. types: [open] → 验证 PR 创建时触发
  2. types: [update] → 验证 PR 源分支新提交时触发
  3. types: [reopen] → 验证 PR 重新打开时触发
  4. types: [merge] → 验证 PR 合并时触发
  5. 不指定 types → 验证默认 [open, reopen, update] 行为
  6. types: [opened]（GitHub 命名）→ 验证报错或明确行为
预期结果: GitCode types 按文档正确触发；GitHub 命名有明确行为
验证点:
  - [正向] 每个 types 值触发对应事件
  - [正向] 默认 types 行为与文档一致
  - [负向] GitHub 命名不应静默忽略
清理:      fixture
