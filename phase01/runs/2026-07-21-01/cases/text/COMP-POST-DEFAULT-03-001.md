用例 ID:   COMP-POST-DEFAULT-03-001
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-028
标题:      post 阶段的 run_always 默认行为：验证成功/失败/取消三种场景

前置条件:
  - workflow 含 post 阶段和 main job

操作步骤:
  1. main job 成功（exit 0）→ 观察 post 是否执行
  2. main job 失败（exit 1）→ 观察 post 是否执行（默认 run_always=true）
  3. 若支持 run_always=false → main 失败时 post 不执行

预期结果:
  - run_always=true（默认）：无论成败都执行 post
  - run_always=false：仅成功时执行 post
  - 文档声明与实测行为一致

验证点:
  - [正向] main 成功 → post 执行
  - [正向] main 失败 → post 仍执行（默认 run_always=true）
  - [正向] 文档 run_always 默认值声明与实测一致

清理:      none
