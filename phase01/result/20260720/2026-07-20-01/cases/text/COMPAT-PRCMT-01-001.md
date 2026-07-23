用例 ID:   COMPAT-PRCMT-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-023
标题:      pull_request_comment 事件：GitCode 独有触发事件

前置条件: 仓库有 pull_request_comment workflow
操作步骤:
  1. PR 评论 → 触发 pull_request_comment
  2. Issue 评论 → 触发 issue_comment 但不触发 pull_request_comment
  3. comments 正则过滤 → 验证正确匹配
预期结果: PR 评论事件正确触发；不与其他事件冲突
验证点:
  - [正向] PR 评论触发事件
  - [正向] 正则过滤正确
  - [负向] 不误触发 issue_comment
清理:      fixture
