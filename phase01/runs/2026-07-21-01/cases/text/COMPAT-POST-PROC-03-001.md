用例 ID:   COMPAT-POST-PROC-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-071
标题:      post 顶层后处理阶段（GitCode 独有）vs GitHub 仅 action 内 post

前置条件:
  - workflow 含 post 后处理步骤
  - main job 可能成功或失败

操作步骤:
  1. 定义 post 阶段（run_always: true）执行清理 echo
  2. main job 执行 exit 0（成功场景）→ 观察 post 是否执行
  3. main job 执行 exit 1（失败场景）→ 观察 post 是否仍执行
  4. 手动取消 workflow → 观察 post 是否执行

预期结果:
  - main 成功时 post 执行（清理正常）
  - main 失败且 run_always=true 时 post 仍执行
  - 手动取消时 post 行为需明确（GitHub post action hook 在取消时也会执行）
  - 此为 GitCode 独有增强，迁移回 GitHub 需改写为 cleanup job

验证点:
  - [正向] main 成功 → post 执行
  - [正向] main 失败 + run_always=true → post 执行
  - [正向] 文档标注 post 为 GitCode 特有

清理:      fixture
