用例 ID:   COMP-ACT-03-014
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P2
溯源意图:  INTENT-ACT-014
母意图:    —
标题:      codecov 覆盖率上报——文件路径/自动发现/token 认证/无 token 公开仓库/日志脱敏

前置条件:
  - 仓库配置了 Codecov 覆盖率上报 workflow
  - 仓库中有覆盖率报告文件（如 `coverage/lcov.info`）
  - 配置了 Codecov token（通过 secret 传入，可选）

操作步骤:
  1. 配置 workflow 使用 `uses: codecov-action`，指定覆盖率文件路径 `coverage/lcov.info`
  2. 触发 workflow，验证覆盖率文件上传成功
  3. 不指定覆盖率文件路径，验证是否能自动发现常见文件
  4. 使用 Codecov token（通过 secret 传入）上传，验证认证成功
  5. 不提供 token，验证公开仓库上传是否可用
  6. 指定不存在的覆盖率文件路径，观察报错
  7. 检查日志中 token 是否被脱敏
  8. 上传大于 1MB 的覆盖率文件，验证行为

预期结果:
  - 指定路径的覆盖率文件上传成功
  - 自动发现可找到常见覆盖率文件
  - token 认证上传成功
  - 无 token 公开仓库上传可用
  - 文件不存在时报错清晰
  - 日志中 token 被脱敏

验证点:
  - [正向] 覆盖率文件上传成功
  - [正向] 自动发现覆盖率文件
  - [正向] token 认证生效
  - [负向] 日志不含 token 明文
  - [负向] 文件不存在时报错清晰
  - [状态] 若 Codecov API 大陆不可达——标记为 blocked-by-network

清理: fixture
