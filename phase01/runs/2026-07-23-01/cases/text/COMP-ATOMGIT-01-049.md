用例 ID:   COMP-ATOMGIT-01-049
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-566~570
母意图:    —
标题:      atomgit 边界格式校验

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 step 中校验 atomgit.sha 长度、ref 格式、ref_name 无前缀等边界条件
  2. 运行 workflow 并断言格式

预期结果:
  - atomgit.sha 长度为 40，atomgit.ref 以 refs/ 开头，atomgit.ref_name 不含 refs/ 前缀，atomgit.actor 非空

验证点:
  - [正向] sha 长度等于 40
  - [正向] ref 以 refs/ 开头
  - [正向] ref_name 不含 refs/ 前缀
  - [正向] actor 非空

清理:      重置 fixture 仓库
