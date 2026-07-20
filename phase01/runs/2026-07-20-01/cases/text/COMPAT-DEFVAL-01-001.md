用例 ID:   COMPAT-DEFVAL-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-014
标题:      默认值差异：defaults.run.shell 与默认 permissions

前置条件: 仓库有 workflow，未指定 defaults.run.shell 和 permissions
操作步骤:
  1. 不指定 shell → 验证 run: 在 bash 中执行
  2. run: exit 1 → 验证 step 标记为失败（bash -e 行为）
  3. 不声明 permissions → 验证 ATOMGIT_TOKEN 实际权限范围
预期结果: 未指定 shell 时用 bash -e；默认 permissions 行为文档化
验证点:
  - [正向] 未指定 shell 时使用 bash
  - [正向] exit 1 导致 step 失败
  - [正向] 默认 permissions 行为可观测
清理:      fixture
