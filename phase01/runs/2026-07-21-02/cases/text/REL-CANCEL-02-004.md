用例 ID:   REL-CANCEL-02-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-037
标题:      手动取消时运行中 step 进程的终止信号与 grace period 行为

前置条件:
  - 仓库配置了支持长时间运行的 fixture
  - workflow 含一个持续运行 step（如 sleep 300s）并在后台启动子进程
  - workflow 配置了 post 清理阶段，用于打印清理标记并回收残留子进程

操作步骤:
  1. 触发该 workflow 运行
  2. 在 step 进入 running 状态约 30s 后，手动执行 Cancel 操作
  3. 观测 step 进程收到的终止信号序列、子进程残留情况、post 清理标记是否出现
  4. 记录从 Cancel 到 runner 可调度新 job 的时间

预期结果:
  - 取消时系统先向 step 进程组发送 SIGTERM，给予合理 grace period
  - grace period 内进程仍未退出，则再发送 SIGKILL 强制终止
  - workflow post 阶段与 action runs.post 清理钩子被调用，日志可见清理标记
  - runner 在取消后合理时限内释放并可复用

验证点:
  - [正向] post 清理标记出现在运行日志中
  - [负向] 运行中 step 不应在取消瞬间被无 grace period 的 SIGKILL 直接杀死
  - [负向] 不应仅 SIGTERM 后永不 SIGKILL 导致 runner 被僵尸进程长期占用
  - [非功能] SIGTERM 到 SIGKILL 的间隔有界（容差 ≤15s）；runner 在取消后 60s 内可调度新 job

清理:      fixture
