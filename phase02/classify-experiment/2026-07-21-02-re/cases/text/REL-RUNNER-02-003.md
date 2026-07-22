用例 ID:   REL-RUNNER-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-014
标题:      前一个 job 的 workspace 文件残留不污染下一次调度的新 job

前置条件:
  - 同 workflow 内两个串行 job（needs 依赖）
  - job A 创建标记文件 /tmp/cross-job-marker 和自定义 env

操作步骤:
  1. job A：创建 marker 文件 + 写 job 级 env 变量
  2. job B（needs: [job A]）：检查 marker 文件不存在、env 变量不存在
  3. 验证 workspace 文件隔离

预期结果:
  - job B workspace 中不存在 job A 创建的 marker 文件
  - job B 环境变量中不含 job A 的自定义 env

验证点:
  - [正向] job B 的 workspace 无 job A 残留文件
  - [正向] job B 环境无 job A 自定义 env
  - [负向] 不应出现跨 job 文件泄露

清理:      fixture
