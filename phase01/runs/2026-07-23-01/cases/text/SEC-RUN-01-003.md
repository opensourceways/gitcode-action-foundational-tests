用例 ID:   SEC-RUN-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-022
母意图:    —
标题:      自托管 Runner 跨项目残留必须被隔离

前置条件:
  - 自托管 runner 被多个项目共享

操作步骤:
  1. 项目 A 的 workflow 写入临时文件和环境变量
  2. 项目 B 的 workflow 在同一 runner 上检查残留

预期结果:
  - 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量
  - runner 清理失败时应标记为不可用

验证点:
  - [负向] 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量
  - [非功能] runner 清理失败时应标记为不可用，避免调度下一 job

清理:      重置 full_instance
