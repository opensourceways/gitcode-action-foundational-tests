用例 ID:   COMP-TRIG-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-001
母意图:    —
标题:      验证 8 种触发事件类型的实际可用性

前置条件:
  - 仓库无特殊设置
  - 准备覆盖 push / pull_request / pull_request_target / issue_comment / pull_request_comment / workflow_dispatch / workflow_call / schedule 共 8 种事件

操作步骤:
  1. 分别为每种事件类型创建对应的 workflow 文件
  2. 按文档声明的语义触发每种事件：push→推送分支、pull_request→创建PR、pull_request_target→fork PR、issue_comment→创建评论、pull_request_comment→PR评论、workflow_dispatch→手动触发、workflow_call→被其他workflow调用、schedule→cron定时
  3. 观察每种事件是否成功创建 workflow 运行记录
  4. 特别验证：schedule 是否实际工作（已有 S3×24+TC-391 FAIL 线索）

预期结果:
  - 每种事件类型均成功创建 workflow 运行记录（run ID 可枚举）
  - pull_request_target 使用目标分支 workflow 文件版本执行
  - workflow_dispatch 的 inputs 值正确注入
  - workflow_call 调用方通过 with/secrets 传参正确接收
  - schedule 按 cron 表达式在 UTC 时区触发

验证点:
  - [正向] 8 种事件类型均产生可追踪的 Run ID
  - [正向] pull_request_target 使用 base 分支 workflow 版本
  - [正向] workflow_dispatch inputs 正确注入
  - [正向] workflow_call 传参正确接收
  - [负向] schedule 应实际触发（已有 FAIL 线索需确认）

清理:      fixture
