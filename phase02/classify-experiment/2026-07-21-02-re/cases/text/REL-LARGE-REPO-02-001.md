用例 ID:   REL-LARGE-REPO-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-032
母意图:    —
标题:      超大仓库 checkout 的磁盘/时间边界

前置条件:
  - 存在一个大于 1GB 的测试仓库

操作步骤:
  1. 触发 workflow 对该大仓库执行 checkout
  2. 观察 checkout 耗时与磁盘占用
  3. 检查是否因超时或磁盘满而失败

预期结果:
  - checkout 应在合理时间内完成
  - 磁盘占用不应超出 runner 配额

验证点:
  - [正向] checkout 成功
  - [nonfunctional] 耗时 < 600 秒
  - [负向] 无磁盘满报错

清理:      重置 fixture 仓库
