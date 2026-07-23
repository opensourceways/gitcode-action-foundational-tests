用例 ID:   REL-FAULT-01-004
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-032
母意图:    —
标题:      故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

前置条件:
  - 仓库已启用 Actions
  - runner 可正常生成 artifact 文件
  - 具备网络分区注入能力

操作步骤:
  1. 创建 workflow，先生成测试 artifact 文件，再执行 upload-artifact 步骤
  2. 触发 workflow 运行
  3. 在 artifact 上传步骤期间注入网络分区，持续 30 秒
  4. 观察运行结果与错误信息

预期结果:
  - artifact 上传步骤失败，job 整体状态为 FAILED
  - 错误信息明确包含网络相关提示（如 timeout、network unreachable、connection reset）
  - 失败前已生成的本地 artifact 文件不受影响（若后续步骤读取）

验证点:
  - [正向] job 状态为 FAILED
  - [正向] 错误信息含网络错误关键词
  - [负向] 不生成不完整或损坏的远端 artifact

清理:      重置 full_instance
