用例 ID:   COMPAT-PR-COMM-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-023
标题:      pull_request_comment 事件：验证 GitCode 独有触发事件类型的语义正确性

前置条件:
  - 配置 pull_request_comment 事件监听
  - 配置 comments 正则过滤

操作步骤:
  1. 在 PR 中发表评论 → 验证 pull_request_comment 触发
  2. 在 Issue 中发表评论 → 验证 pull_request_comment 不触发
  3. 测试 comments 正则过滤（匹配/排除不同内容）
  4. 验证 payload 中 atomgit.event.* 字段完整性
  5. 确认同一评论不重复触发 pull_request_comment 和 issue_comment

预期结果:
  - pull_request_comment 仅在 PR 评论时触发
  - Issue 评论触发 issue_comment 但不触发 pull_request_comment
  - comments 正则正确过滤
  - payload 结构完整

验证点:
  - [正向] PR 评论时触发 pull_request_comment
  - [正向] Issue 评论时不触发 pull_request_comment
  - [正向] comments 正则过滤正确
  - [负向] 同一评论不应同时触发两个事件

清理:      fixture
