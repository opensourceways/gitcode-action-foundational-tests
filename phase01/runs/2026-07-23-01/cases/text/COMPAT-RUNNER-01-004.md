用例 ID:   COMPAT-RUNNER-01-004
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-008
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      自定义特征标签不被支持时应给出可用标签列表

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，runs-on 使用自定义特征标签（如 `[gpu, nvidia]`）
  2. 提交并触发 workflow

预期结果:
  - 系统应明确提示该标签组合不可用
  - 报错应给出可用标签列表（如官方资源池标签）

验证点:
  - [正向] 报错信息说明标签不匹配
  - [正向] 报错给出可用标签列表或标签格式指引

清理:      无
