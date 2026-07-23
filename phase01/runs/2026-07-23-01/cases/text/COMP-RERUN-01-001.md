用例 ID:   COMP-RERUN-01-001
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-009
母意图:    —
标题:      rerun 后 atomgit.sha 保持原始值 run_number 递增

前置条件:
  - 存在一条已完成的 workflow 运行

操作步骤:
  1. 记录原始运行的 sha、ref、run_number
  2. 执行 rerun
  3. 对比新运行与原始运行的上下文

预期结果:
  - sha、ref、event_name 保持原始值
  - run_number 更新为新值（递增）

验证点:
  - [正向] rerun 后 sha 与原始运行一致
  - [正向] rerun 后 run_number 大于原始值

清理:      none
