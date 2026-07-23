用例 ID:   COMPAT-ISOLATE-01-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-028
母意图:    —
标题:      Runner 环境隔离——跨 job 文件隔离

前置条件:
  - 平台提供多 job 工作流执行能力
  - Runner 为官方托管资源池或等效隔离环境

操作步骤:
  1. 在 job A 中于 workspace 和 /tmp 写入唯一标记文件
  2. 在 job B 中尝试读取 job A 写入的标记文件
  3. 验证 job B 无法访问 job A 的文件残留

预期结果:
  - job B 无法读取到 job A 在 workspace 或 /tmp 中写入的文件
  - 每个 job 获得独立的文件系统视图
  - 隔离行为与 GitHub Actions 的 job 级隔离语义一致

验证点:
  - [负向] job B 中不存在 job A 的 workspace 标记文件
  - [负向] job B 中不存在 job A 的 /tmp 标记文件
  - [正向] 系统为每个 job 提供独立执行环境

清理:      fixture
