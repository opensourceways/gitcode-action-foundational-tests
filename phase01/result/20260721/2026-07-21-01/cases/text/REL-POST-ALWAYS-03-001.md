用例 ID:   REL-POST-ALWAYS-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-046
标题:      post 阶段在 main job 失败时仍执行（run_always=true）——通知/清理可靠性

前置条件:
  - workflow 配置 post 阶段（run_always=true）
  - main job 故意 exit 1

操作步骤:
  1. 配置 main job 执行 exit 1（模拟失败）
  2. post 阶段 run_always=true 执行清理 echo
  3. 观察 post 是否在 main job 失败后执行

预期结果:
  - main job 失败后 post 阶段步骤执行
  - post 日志完整可见
  - cleanup 操作被执行

验证点:
  - [正向] main job 失败后 post 执行
  - [正向] post 日志可见 cleanup done

清理:      none
