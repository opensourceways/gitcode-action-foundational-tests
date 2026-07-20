用例 ID:   SEC-RUNNER-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-025
母意图:    —
标题:      fork PR 触发的 pull_request workflow 不应有持久的 runner 状态残留

前置条件:
  - 第一个 fork PR workflow 在 runner 上写入文件、设置环境变量、启动后台进程
  - 第二个内部 job 在同一 runner 上执行

操作步骤:
  1. fork PR job 在 $GITHUB_WORKSPACE 创建文件 /tmp/secret-residue.dat
  2. fork PR job export 环境变量 MALICIOUS_ENV=evil
  3. fork PR job 结束后，内部 push job 在同一 runner 上执行
  4. 检查是否能看到前 job 残留文件、环境变量、进程

预期结果:
  - fork PR job 结束后工作区、环境变量、后台进程被完全清理
  - 后续内部 job 不应能看到 fork PR job 的任何残留

验证点:
  - [负向] 后续 job 不应看到 /tmp/secret-residue.dat
  - [负向] 后续 job env 中不含 MALICIOUS_ENV
  - [负向] fork PR job 启动的后台进程在结束后被终止

清理: full_instance
