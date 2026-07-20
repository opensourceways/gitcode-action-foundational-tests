用例 ID:   COMPAT-POST-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-018
标题:      post 后处理阶段：验证 run_always 默认行为 + 与 always() 的交互

前置条件:
  - workflow 包含 post 阶段
  - post 中 run_always: true（默认）或 false

操作步骤:
  1. 测试 run_always: true 时主流程失败后排 post 仍执行
  2. 测试 run_always: false 时主流程失败后 post 不执行
  3. 测试 post 中步骤可发送通知/上传 artifact
  4. 测试 post 失败是否影响 workflow 最终结论
  5. 测试 post 中能否访问前置 job 的 outputs

预期结果:
  - run_always: true 时 post 始终执行
  - run_always: false 时仅在成功时执行
  - post 失败不影响 workflow 最终状态

验证点:
  - [正向] run_always: true → workflow 失败后 post 仍执行
  - [正向] run_always: false → workflow 失败后 post 不执行
  - [正向] post 中步骤可正常执行 artifact/通知操作
  - [负向] post 失败不应将 workflow 标记为 failure

清理:      fixture
