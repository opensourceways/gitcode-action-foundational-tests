用例 ID:   REL-RES-MEM-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-041
标题:      container.options --memory 限制生效：容器内存超限时被 OOM kill

前置条件:
  - container.options: --memory 512m
  - step 执行超过 512MB 的内存分配

操作步骤:
  1. 配置 container.options: --memory 512m
  2. step 执行 stress --vm 1 --vm-bytes 1G
  3. 观察容器内进程是否被 OOM kill

预期结果:
  - 超过 --memory 限制时进程被 oom-kill
  - 日志含 OOM 信息
  - 容器内存限制生效

验证点:
  - [正向] 超过限制时进程被 kill
  - [正向] 日志含 OOM 信息

清理:      fixture
