用例 ID:   COMP-POST-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-010
标题:      验证 post 后处理阶段 run_always 与时序保证

前置条件:
  - 配置 post 阶段（默认 run_always: true）

操作步骤:
  1. 主流程成功 + run_always: true → post 执行
  2. 主流程失败 + run_always: true → post 仍执行
  3. 主流程成功 + run_always: false → post 执行
  4. 主流程失败 + run_always: false → post 不执行
  5. 主流程被取消 + run_always: true → 观察行为

预期结果:
  - run_always: true 时 post 始终执行
  - run_always: false 时仅成功执行
  - post 在全部 stage 完成后执行

验证点:
  - [正向] 成功+run_always:true → post 执行
  - [正向] 失败+run_always:true → post 仍执行
  - [正向] 成功+run_always:false → post 执行
  - [正向] 失败+run_always:false → post 不执行
  - [非功能] 取消+run_always:true 时行为可观测

清理:      fixture
