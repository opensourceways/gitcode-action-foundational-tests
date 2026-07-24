用例 ID:   COMPAT-PR-01-005
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-003
母意图:    —
标题:      PR paths 过滤不工作时的兼容性差异

前置条件:
  - 仓库已启用 Actions
  - 存在至少一个已配置的 workflow，on 包含 pull_request.paths
  - 测试者持有 maintainer 权限

操作步骤:
  1. 配置 workflow 触发器为 `pull_request.paths: ['api/**']`
  2. 创建一个修改 `api/` 路径文件的 PR
  3. 观察是否触发对应 workflow 运行

预期结果:
  - GitHub 行为：修改匹配路径的 PR 应触发 workflow
  - GitCode 实际：满足 paths 条件的 PR 变更没有对应 workflow 运行（已知问题）
  - 差异应被记录

验证点:
  - [负向] 不通过 PR 修改匹配路径后无 workflow 触发
  - [正向] 若平台已修复，匹配路径的 PR 应触发 workflow

清理:      无
