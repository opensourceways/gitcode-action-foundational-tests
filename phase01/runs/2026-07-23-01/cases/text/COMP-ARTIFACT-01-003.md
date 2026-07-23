用例 ID:   COMP-ARTIFACT-01-003
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-015
母意图:    —
标题:      artifact 保留期设置生效

前置条件:
  - workflow 设置 retention-days: 1

操作步骤:
  1. 上传 artifact 并设置 retention-days: 1
  2. 等待超过保留期后尝试下载

预期结果:
  - 超过保留期后 artifact 不可下载

验证点:
  - [正向] 保留期内可下载 artifact
  - [负向] 超过保留期后下载返回 404

清理:      none
