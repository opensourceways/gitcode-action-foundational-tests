# 用例归档

用例 ID:   COMPAT-CONCUR-01-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-034
母意图:    —
标题:      concurrency cancel-in-progress false 时应排队而非报错

前置条件:
  - 仓库已启用 workflow
  - 同一 concurrency group 当前无运行中实例或可通过快速触发制造冲突

操作步骤:
  1. 创建一个 workflow_dispatch 触发的 workflow
  2. 配置 workflow 级 `concurrency` 块，指定 group 名称和 `cancel-in-progress: false`
  3. 在 job 中加入一个长时间运行的 step（如 sleep 60）
  4. 快速连续触发两次该 workflow
  5. 观察第二次触发的行为

预期结果:
  - 第二次触发不应直接报错失败
  - 第二次触发应进入排队（pending/queued）状态，等待第一次完成后执行
  - 这与 GitHub Actions 的排队语义一致

验证点:
  - [负向] 第二次触发不应被标记为失败或取消
  - [正向] 第二次触发的状态为 queued / pending
  - [正向] 第一次完成后第二次正常开始执行

清理:      重置 fixture 仓库
