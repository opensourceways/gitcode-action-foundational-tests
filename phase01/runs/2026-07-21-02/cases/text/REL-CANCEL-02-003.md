用例 ID:   REL-CANCEL-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-018
标题:      Post 后处理阶段在 workflow 被取消时仍应执行（run_always: true）

前置条件:
  - workflow 包含 post 阶段（step=echo "cleanup done"）
  - post 使用默认 run_always: true

操作步骤:
  1. 触发 workflow 后手动取消正在执行的 run
  2. 验证 post 阶段的 step 日志可见于 Run 详情
  3. 验证 post 阶段的 step 正常完成

预期结果:
  - post 阶段在 workflow 被取消后仍执行
  - post step 完成（不被跳过）

验证点:
  - [正向] 手动取消后 post 阶段仍执行
  - [正向] post step 正常完成
  - [负向] post 不因主流程被取消而跳过

清理:      fixture
