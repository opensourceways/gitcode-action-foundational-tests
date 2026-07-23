用例 ID:   SEC-ISOL-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-025
母意图:    —
标题:      fork PR 触发的 pull_request workflow 不应有持久的 runner 状态残留

前置条件:
  - 仓库配置了 pull_request 和 push 触发器
  - 存在一个来自 fork 的 PR
  - 同一 runner 可能被多个 job 复用（非 ephemeral 或复用场景）

操作步骤:
  1. fork PR 的 job A 在 runner 上执行，在工作区写入标记文件 `cross-job-marker`，设置自定义环境变量 `FORK_JOB_ENV=residue`，启动后台进程 `sleep 9999 &`
  2. job A 完成后，同 runner 上启动内部 push 触发的 job B
  3. job B 中检查：(a) 工作区是否存在 `cross-job-marker` 文件，(b) 环境变量中是否包含 `FORK_JOB_ENV`，(c) fork job 的后台进程是否仍在运行
  4. 若 runner 是 ephemeral（一次性），job B 应工作在全新环境中

预期结果:
  - job B 的工作区中不应存在 job A 创建的 `cross-job-marker` 文件
  - job B 的环境变量中不应包含 `FORK_JOB_ENV`
  - job A 启动的后台进程不应在 job B 执行期间存活
  - 若 runner 复用，清理必须在 job 间完成

验证点:
  - [负向] 后续 job 不应能看到前一个 fork PR job 创建的工作区文件
  - [负向] 后续 job 的环境变量中不应包含前一个 fork PR job 的 export 变量
  - [负向] fork PR job 启动的后台进程在 job 结束后应被终止
  - [正向] 后续 job 中 `ls $ATOMGIT_WORKSPACE` 显示干净的 checkout 目录

清理:      full_instance
