用例 ID:   COMPAT-OUTPUTS-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-030
标题:      job outputs 传递协议对标

前置条件: 仓库多 job workflow，已知 TC-486 needs 指向 matrix job 有 bug
操作步骤:
  1. step 通过 ATOMGIT_OUTPUT 设置输出 → 验证同 job 后续 step 可读
  2. job.outputs 声明 → 验证下游 needs job 可读
  3. matrix job outputs → 验证 needs 可引用
  4. 多行 outputs → 验证正确传递

预期结果: outputs 三级传递链正确；matrix outputs 可被 needs 引用
验证点:
  - [正向] ATOMGIT_OUTPUT 协议正确
  - [正向] job.outputs 跨 job 传递
  - [正向] matrix outputs 可引用
清理:      fixture
