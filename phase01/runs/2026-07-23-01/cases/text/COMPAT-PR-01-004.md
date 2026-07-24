用例 ID:   COMPAT-PR-01-004
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-003
母意图:    —
标题:      PR types 含 merge 时不触发与 GitHub 行为差异

前置条件:
  - 仓库已启用 Actions
  - 存在至少一个已配置的 workflow，on 包含 pull_request.types 且含 merge
  - 测试者持有 maintainer 权限

操作步骤:
  1. 配置 workflow 触发器为 `pull_request.types: [open, merge]`
  2. 合并一个 PR
  3. 观察是否触发对应 workflow 运行

预期结果:
  - GitHub 行为：合并 PR 应触发 pull_request 的 merge 独立 Job
  - GitCode 实际：合并后只出现 PUSH 运行（已知问题）
  - 差异应被记录

验证点:
  - [负向] 不通过仅产生 PUSH 运行而无 pull_request 运行
  - [正向] 若平台已修复，合并 PR 后应触发 pull_request 类型运行

清理:      无
