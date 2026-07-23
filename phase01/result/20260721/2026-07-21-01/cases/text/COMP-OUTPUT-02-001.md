用例 ID:   COMP-OUTPUT-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-008
标题:      验证 outputs 三级传递链 step → job → workflow

前置条件:
  - jobA 的 step 通过 ATOMGIT_OUTPUT 写入 key=value
  - jobA 声明 outputs 映射
  - jobB 通过 needs 读取

操作步骤:
  1. step output → 同 job 后续 step 通过 steps 上下文可读
  2. step output → job outputs 映射 → needs 下游可读
  3. workflow_call outputs → 调用方可读
  4. 多行值通过 heredoc 分隔符传递
  5. 引用不存在的 needs.<id>.outputs.<key>

预期结果:
  - 三级映射链完整
  - 多行值正确处理
  - 引用不存在 output 时报错

验证点:
  - [正向] 三级链每级正确传递
  - [正向] 多行值正确传递
  - [负向] 引用不存在 output 明确报错

清理:      fixture
