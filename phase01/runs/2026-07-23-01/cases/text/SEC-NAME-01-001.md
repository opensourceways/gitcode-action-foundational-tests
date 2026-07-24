用例 ID:   SEC-NAME-01-001
维度标签:   [security, compatibility]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-024
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      Secret/变量名含特殊字符时不可导致意外求值或权限绕过

前置条件:
  - 仓库配置了含中划线的 secret MY-VAR

操作步骤:
  1. 提交一个 workflow，引用 secrets.MY-VAR 并在 shell 中使用
  2. 触发 workflow 并查看运行日志

预期结果:
  - 含中划线的 secret 不应因解析错误而被泄露到日志
  - 若不支持中划线，应在 YAML 校验阶段报错

验证点:
  - [负向] 含中划线的 secret 绝不应因解析错误而被泄露到日志或环境变量
  - [非功能] 若不支持中划线，应在 YAML 校验阶段报错，而非运行期静默失败

清理:      重置 fixture 仓库
