用例 ID:   COMP-OUTPUT-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-008
标题:      验证 outputs 三级传递链: step → job → workflow
前置条件:  仓库无特殊设置
操作步骤:
  1. step 通过 $ATOMGIT_OUTPUT 写入 key=value
  2. job 通过 outputs 映射暴露
  3. 下游 job 通过 needs.<id>.outputs.<key> 读取
  4. workflow_call 场景验证 workflow 级 outputs
预期结果:
  - step → job → needs 三级传递链完整闭合
  - 多行值通过 heredoc 正确传递
  - 引用不存在的 outputs 明确报错
验证点:
  - [正向] step output → job outputs → 下游 needs 可读
  - [正向] 多行值正确传递
  - [负向] 不存在的 outputs 引用应报错
清理:      fixture
