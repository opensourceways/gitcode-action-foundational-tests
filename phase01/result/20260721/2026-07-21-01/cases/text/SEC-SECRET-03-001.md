用例 ID:   SEC-SECRET-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-045
母意图:    —
标题:      Secret 全生命周期管理——创建、更新、删除、过期

前置条件:
  - 仓库可管理 Secret
  - 有 workflow 引用目标 Secret

操作步骤:
  1. 创建 Secret DEPLOY_KEY=value_v1，触发 workflow 读取该值
  2. 更新 Secret DEPLOY_KEY=value_v2，再次触发 workflow
  3. 删除 Secret DEPLOY_KEY，再次触发 workflow
  4. 验证各阶段行为正确

预期结果:
  - 创建后立即可在 workflow 中引用
  - 更新后新 workflow run 使用新值（不应缓存旧值）
  - 删除后引用该 secret 的 job 收到空值或错误
  - 过期 token 不可恢复使用

验证点:
  - [正向] 创建后 echo ${{ secrets.DEPLOY_KEY }} 返回有效值
  - [正向] 更新后新 run 使用新值
  - [负向] 删除后 echo 返回空
  - [负向] 过期 token 不可通过缓存恢复

清理: fixture
