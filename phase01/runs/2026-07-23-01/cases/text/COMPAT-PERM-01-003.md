用例 ID:   COMPAT-PERM-01-003
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-030
母意图:    —
标题:      permissions 命名差异——GitHub contents 权限项应报错

前置条件:
  - 仓库支持 permissions 字段解析

操作步骤:
  1. 在工作流中声明 `permissions: { contents: read }`
  2. 提交并推送，观察平台解析行为
  3. 确认平台是否拒绝 GitHub 风格的权限命名

预期结果:
  - 平台在解析阶段报错，提示 `contents` 不是可识别的权限项
  - 不应静默忽略该权限项后继续执行
  - 报错信息应清晰指出未知的权限域名称

验证点:
  - [负向] 使用 `contents` 时 workflow 解析/校验阶段应报错
  - [正向] 错误信息应明确提示 unknown property 或类似说明
  - [负向] 不应静默忽略导致实际权限与开发者预期不符

清理:      fixture
