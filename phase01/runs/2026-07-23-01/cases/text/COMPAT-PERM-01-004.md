用例 ID:   COMPAT-PERM-01-004
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-030
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    COMPAT-PERM-01-003
标题:      permissions 命名差异——GitCode repository 权限项正常生效

前置条件:
  - 仓库支持 permissions 字段解析
  - 平台已配置 repository 权限域

操作步骤:
  1. 在工作流中声明 `permissions: { repository: read }`
  2. 在工作流步骤中执行 clone 或读取仓库内容的操作
  3. 验证权限正常生效，工作流可完成仓库读取

预期结果:
  - `repository: read` 被平台正确解析并生效
  - 工作流可正常执行 clone 和读取仓库内容
  - GitCode 风格的权限命名与平台语义一致

验证点:
  - [正向] workflow 解析阶段无报错
  - [正向] 工作流成功执行仓库读取操作
  - [正向] repository 权限项语义与 GitCode 平台预期一致

清理:      fixture
