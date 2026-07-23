用例 ID:   REL-YAMLCACHE-01-060
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-060
母意图:    —
标题:      Workflow YAML 缓存失效——修改后无旧代码残留

前置条件:
  - 仓库具备 workflow 修改与触发权限

操作步骤:
  1. 第一轮执行记录输出 marker_v1
  2. 修改 workflow 输出为 marker_v2 并 push
  3. 立即触发 workflow

预期结果:
  - 新触发运行日志中出现 marker_v2
  - 不应出现 marker_v1 缓存残留

验证点:
  - [正向] 日志打印 marker_v2
  - [负向] 不应打印 marker_v1

清理:      重置 fixture 仓库
