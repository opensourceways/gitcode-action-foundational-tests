用例 ID:   COMP-WFLOW-01-064
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-366~401
母意图:    —
标题:      workflow stages 阶段结构字段验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 定义含 stages 的 workflow，使用 map 格式
  2. 验证 stage 间串行和 fail_fast

预期结果:
  - stages 为 map 格式，每个 stage 含 jobs，stage 间串行执行，fail_fast 控制失败时是否中断

验证点:
  - [正向] stages map 格式通过校验
  - [正向] 单 stage 可缺省 stages 字段
  - [正向] fail_fast true 时某 job 失败中断后续 stage

清理:      重置 fixture 仓库
