用例 ID:   COMPAT-RUNNER-01-006
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-011
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 未预装 Java 工具链与 GitHub 差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，在 run 步骤中执行 `java -version` 和 `mvn -version`
  2. 触发 workflow

预期结果:
  - GitHub 行为：Runner 预装 Java 或通过 setup-java 安装
  - GitCode 行为：Runner 未预装 Java，且 setup-java 插件不存在
  - 差异应被记录

验证点:
  - [正向] 系统对缺失的 Java 工具链给出明确提示
  - [正向] 提示应建议替代方案（如使用自定义 Runner 或预装环境）

清理:      无
