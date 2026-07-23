用例 ID:   SEC-MASK-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-005
母意图:    —
标题:      Secret 值直接 echo 到日志时应被脱敏为 `***`

前置条件:
  - 仓库配置了项目级 Secret DEPLOY_TOKEN（值已知，如 `test-secret-value-2026`）
  - workflow 在非 fork 场景下可访问 Secret（使用 push 触发）

操作步骤:
  1. 提交 workflow，在 job 中直接 `echo "${{ secrets.DEPLOY_TOKEN }}"` 到日志
  2. 在另一 step 中通过 env 变量间接 `echo $DEPLOY_TOKEN`
  3. 在同一 job 内多次引用同一 Secret，每次 echo 输出
  4. 通过 API 拉取 job 日志，搜索已知 Secret 明文

预期结果:
  - 所有 `echo ${{ secrets.DEPLOY_TOKEN }}` 的输出在日志中被替换为 `***`
  - 通过 env 变量间接引用的输出同样被脱敏为 `***`
  - 同一 job 内多次引用，每次出现均被遮蔽
  - 日志全文搜索 Secret 明文命中数为 0

验证点:
  - [负向] 直接 echo Secret 的日志行中不出现原始 Secret 明文
  - [负向] 通过 env 变量间接 echo 的日志行中不出现原始 Secret 明文
  - [负向] 同一 job 内多次 echo Secret，每次输出均被遮蔽
  - [正向] 非 Secret 文本的 echo 在日志中正常显示

清理:      fixture
