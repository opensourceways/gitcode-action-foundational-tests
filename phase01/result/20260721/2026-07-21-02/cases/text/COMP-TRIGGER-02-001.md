用例 ID:   COMP-TRIGGER-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-001
标题:      验证 8 种触发事件类型均能产生运行记录
incorporates: TC-223~238 (trigger config), TC-561 (PR merge trigger), TC-461/463 (pull_request_target)

前置条件:
  - 每个事件类型配置对应的 workflow 文件

操作步骤:
  1. push: 推送代码到分支
  2. pull_request: 创建 PR（open/reopen/update）
  3. pull_request_target: PR 触发 base 分支 workflow
  4. issue_comment: 在 Issue 上创建评论
  5. pull_request_comment: 在 PR 上创建含特定内容的评论
  6. workflow_dispatch: 手动触发（传入 inputs 参数）
  7. workflow_call: 被另一个 workflow 通过 uses 调用
  8. schedule: 配置 cron 定时触发

预期结果:
  - 每种事件类型成功创建 workflow 运行记录
  - workflow_dispatch inputs 正确注入
  - workflow_call calls + secrets 传参正确
  - schedule 按 cron 表达式在 UTC 时区触发

验证点:
  - [正向] 8 种事件类型均能创建运行记录
  - [正向] PR merge 事件（types: [merge]）应触发对应 workflow
  - [正向] pull_request_target open 事件应可靠触发
  - [正向] schedule 应实际产生运行

清理:      fixture
