用例 ID:   COMP-ISOLATION-01-001
维度标签:   [completeness, reliability, security]
维度:      完备性
优先级:    P0
溯源意图:  INTENT-COMP-011
母意图:    —
标题:      Runner 环境隔离强度验证——跨 job 文件残留不可访问

前置条件:
  - 仓库配置了默认 workflow
  - Runner 为官方托管资源池

操作步骤:
  1. 创建 workflow，job A 在 /tmp 和 workspace 中写入标记文件（含唯一标识内容）
  2. job A 结束后，job B 尝试读取 /tmp 和 workspace 中的标记文件
  3. 同时检查进程列表中是否残留 job A 的进程

预期结果:
  - job B 不应能读取到 job A 在 /tmp 或 workspace 中写入的标记文件
  - job B 的进程列表中不应出现 job A 的残留进程
  - 系统应为每个 job 提供隔离的执行环境

验证点:
  - [负向] job B 中不存在 job A 的 /tmp 标记文件
  - [负向] job B 的 workspace 中不包含 job A 写入的文件
  - [负向] job B 进程列表中无 job A 残留进程

清理:      fixture
