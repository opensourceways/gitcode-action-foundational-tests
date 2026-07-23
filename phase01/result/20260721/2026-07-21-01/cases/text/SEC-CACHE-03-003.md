用例 ID:   SEC-CACHE-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-052
母意图:    —
标题:      Workflow YAML 缓存不应导致旧版本 workflow 被执行

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 修改 workflow YAML 添加唯一标识 step
  2. 推送变更
  3. 触发 workflow 验证是否执行新 YAML 内容

预期结果:
  - 每次触发应使用仓库当前的 workflow YAML 版本
  - 不应使用缓存的旧版本
  - 修改后的 step 应在日志中出现

验证点:
  - [负向] 修改 workflow YAML 后下一次触发应执行新内容
  - [正向] 平台是否有机制确保 YAML 版本一致性

清理:      none
