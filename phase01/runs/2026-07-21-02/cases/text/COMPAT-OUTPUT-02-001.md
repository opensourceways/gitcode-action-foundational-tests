用例 ID:   COMPAT-OUTPUT-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-030
标题:      job outputs 传递：ATOMGIT_OUTPUT 协议对标 + steps.outputs + jobs.outputs 完整性

前置条件:
  - workflow 中有 job A 产生 outputs
  - job B 通过 needs 引用 job A 的 outputs
  - 已知 TC-486：needs 指向 matrix 父 job 导致初始化错误

操作步骤:
  1. step 通过 ATOMGIT_OUTPUT 设置 key=value → 验证 steps.<id>.outputs.key 可读
  2. job.outputs 声明映射 → 验证下游 job 通过 needs.<id>.outputs.key 正确读取
  3. 测试多行 outputs 通过 heredoc 正确传递
  4. matrix job 的 outputs 可被 needs 引用（验证 TC-486 已知 bug）

预期结果:
  - ATOMGIT_OUTPUT 协议正确
  - outputs 三级传递链（step→job→needs job）正确
  - 多行 outputs 不截断

验证点:
  - [正向] step ATOMGIT_OUTPUT → steps.outputs 可读
  - [正向] job.outputs → needs.outputs 正确传递
  - [正向] 多行 heredoc outputs 正确传递
  - [负向] matrix job outputs 被 needs 引用不报初始化错误

清理:      fixture
