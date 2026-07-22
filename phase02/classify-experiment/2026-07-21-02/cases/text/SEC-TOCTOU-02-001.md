用例 ID:   SEC-TOCTOU-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-031
母意图:    —
标题:      TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定

前置条件:
  - 存在已审批的 PR workflow
  - 审批后 PR 又有新 commit 推送

操作步骤:
  1. PR workflow 获得审批并开始运行
  2. 在运行过程中向 PR 推送新 commit
  3. 观察 workflow 是否重新触发并需要重新审批

预期结果:
  - 新 commit 推送后应触发新的 workflow run
  - 新 run 不应继承旧审批，应要求重新审批

验证点:
  - [负向] 新 commit 不导致旧 run 执行未审批代码
  - [正向] 新 run 正确关联最新 commit SHA

清理:      重置 fixture 仓库
