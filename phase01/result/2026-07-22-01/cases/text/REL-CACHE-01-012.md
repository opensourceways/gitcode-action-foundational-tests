用例 ID:   REL-CACHE-01-012
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-060
母意图:    —
标题:      Workflow YAML 缓存失效——修改后无旧代码残留

前置条件:
  - 仓库已启用 Actions
  - workflow 文件位于默认分支

操作步骤:
  1. 创建初始 workflow，job 中执行 `echo "VERSION_A"`
  2. 推送并触发运行，确认日志输出 VERSION_A
  3. 修改同一 workflow 文件，将 `echo "VERSION_A"` 改为 `echo "VERSION_B"`
  4. 再次推送并触发运行
  5. 检查最新运行的日志输出

预期结果:
  - 第二次运行的日志中输出 VERSION_B
  - 日志中不出现 VERSION_A（旧代码不应被缓存执行）
  - 两次运行的 workflow 文件路径与 commit SHA 对应正确

验证点:
  - [正向] 最新运行日志包含 VERSION_B
  - [负向] 最新运行日志不包含 VERSION_A
  - [正向] 两次运行对应的 head_sha 不同

清理:      重置 fixture 仓库
