用例 ID:   SEC-MASK-01-006
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-028
标题:      fork PR 下 ::add-mask:: 注册不影响主分支 job 的 mask 表

前置条件:
  - 仓库配置了 Secret DEPLOY_TOKEN
  - 准备 fork PR workflow 和内部 push workflow
  - fork PR workflow 中使用 ::add-mask:: 注册敏感值

操作步骤:
  1. fork PR workflow 中使用 ::add-mask:: 注册敏感值 FORK_PR_VALUE
  2. 后续在同一 runner 上触发内部 push workflow
  3. 内部 job 中 echo FORK_PR_VALUE
  4. 验证 FORK_PR_VALUE 在内部 job 中是否被遮蔽
  5. 内部 job 中 echo 自己的 Secret DEPLOY_TOKEN → 验证正常遮蔽

预期结果:
  - fork PR job 的 mask 注册仅在 fork PR job 内生效
  - 后续内部 job 不受 fork PR mask 表影响
  - FORK_PR_VALUE 在内部 job 中应显示为明文（未注册 mask）
  - 内部 job 自己的 Secret 正常被遮蔽

验证点:
  - [负向] fork PR 注册的 mask 值在内部 job 中不生效（应显示明文）
  - [正向] 内部 job 自己的 Secret 正常遮蔽
  - [负向] fork PR 的 mask 不跨 job 传播

清理:      fixture
