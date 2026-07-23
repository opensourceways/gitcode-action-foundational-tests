用例 ID:   REL-NET-01-013
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-062
母意图:    —
标题:      网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时

前置条件:
  - 仓库已启用 Actions
  - runner 具备网络访问能力

操作步骤:
  1. 创建 workflow，包含一个 step 使用 curl 访问不可达地址（如 `http://192.0.2.1` 测试网段）
  2. 推送并触发运行
  3. 观察该 step 的失败行为与耗时

预期结果:
  - curl 步骤在合理超时内失败（≤ 120 秒，默认连接超时 + 重试）
  - 错误信息明确提示连接失败（如 Connection timed out、No route to host）
  - 该 step 失败后，若后续步骤声明 `if: ${{ always() }}` 仍可执行

验证点:
  - [正向] 步骤状态为 FAILED，且失败原因含网络错误
  - [非功能] 步骤总耗时 ≤ 120 秒（有界超时）
  - [正向] 后续 always() 步骤正常执行

清理:      重置 fixture 仓库
