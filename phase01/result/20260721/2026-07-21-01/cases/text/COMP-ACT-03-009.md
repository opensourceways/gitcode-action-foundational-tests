用例 ID:   COMP-ACT-03-009
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-009
母意图:    —
标题:      SWR 上传/下载与 ak/sk 认证——已知认证待验证(#72/#73/#74)/日志脱敏

前置条件:
  - 仓库配置了 SWR 镜像仓库相关 workflow
  - 配置了 SWR ak/sk（通过 secret 传入）
  - 已知 ak/sk 认证待验证 (#72, #73, #74)

操作步骤:
  1. 配置 workflow 使用 `uses: official_swr`，提供 ak/sk 进行登录
  2. 登录成功后执行 `docker push` 推送镜像到 SWR
  3. 执行 `docker pull` 从 SWR 拉取刚才推送的镜像
  4. 使用错误的 ak/sk，观察认证失败的报错
  5. 检查 workflow 日志中 ak/sk 是否被脱敏
  6. 推送多个 tag（含 `latest`），验证 tag 管理

预期结果:
  - 正确 ak/sk 登录成功，镜像可 push/pull
  - 错误 ak/sk 时给出认证失败报错（不含密钥明文）
  - 日志中 ak/sk 被脱敏处理
  - 多 tag 推送正常，latest tag 覆盖正常

验证点:
  - [正向] 正确 ak/sk 登录后 push/pull 成功（已知待验证 #72-74）
  - [正向] 错误 ak/sk 时报错清晰且不泄露密钥
  - [负向] 日志不含 ak/sk 明文
  - [状态] 若 SWR 网络不可达——标记为 blocked-by-platform

清理: fixture
