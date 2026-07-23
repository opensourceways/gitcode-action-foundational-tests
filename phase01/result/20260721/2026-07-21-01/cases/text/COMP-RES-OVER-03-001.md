用例 ID:   COMP-RES-OVER-03-001
维度标签:   [completeness, reliability]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-016
标题:      托管 Runner 资源超限行为：内存/磁盘超出规格时的处理

前置条件:
  - 使用 small flavor runner (2核8GB)

操作步骤:
  1. 尝试分配 >8GB 内存的操作
  2. 尝试写满磁盘空间
  3. 观察 OOM kill 是否可观测、磁盘满报错是否清晰

预期结果:
  - OOM 时 job 标记 failure + 日志可见 OOM 信号
  - 磁盘满时给出明确「磁盘不足」报错
  - 不应泛化 failure 无具体原因

验证点:
  - [正向] OOM 时 Run = failure
  - [正向] 日志含 OOM/disk full 明确信息
  - [负向] 不应泛化报错且无具体原因

清理:      fixture
