用例 ID:   COMPAT-RUNNER-01-005
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-008
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      内网环境 Runner 不支持时的差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，runs-on 使用内网环境标签
  2. 提交并触发 workflow

预期结果:
  - 系统应明确提示内网环境 Runner 不可用
  - 不应无限排队

验证点:
  - [正向] 系统对内网标签给出明确报错
  - [负向] 不通过无限排队

清理:      无
