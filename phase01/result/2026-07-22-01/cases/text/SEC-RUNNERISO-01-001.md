用例 ID:   SEC-RUNNERISO-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-022
母意图:    —
标题:      自托管 Runner 跨项目残留应被隔离

前置条件:
  - 自托管 Runner 被多个项目共享
  - 项目 A 与项目 B 均使用同一 Runner

操作步骤:
  1. 在项目 A 的 workflow 中向 Runner 本地磁盘写入敏感文件
  2. 随后在项目 B 的 workflow 中检查 Runner 本地磁盘是否存在项目 A 的残留文件
  3. 观察项目 B workflow 执行结果

预期结果:
  - 项目 B 的 workflow 无法访问项目 A 遗留的敏感文件
  - Runner 本地工作目录按项目或运行实例隔离
  - 系统保证多项目共享 Runner 时的数据隔离

验证点:
  - [负向] 项目 B 未读取到项目 A 的残留敏感文件
  - [负向] Runner 磁盘不存在跨项目数据残留
  - [正向] 系统返回隔离正常或文件不存在的提示

清理:      重置 fixture 仓库（如涉及多项目需全实例重置）
