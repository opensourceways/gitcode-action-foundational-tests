用例 ID:   COMPAT-SECRET-01-005
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-002
母意图:    —
标题:      环境级 secrets 不支持时应明确报错而非降级为项目级

前置条件:
  - 仓库已启用 Actions
  - 已配置项目级 secret PROJECT_SECRET
  - 未配置环境级 secret（或环境 secrets 功能不可用）

操作步骤:
  1. 创建一个 workflow，其中 job 声明 `environment: prod` 并引用 `${{ secrets.ENV_SECRET }}`
  2. 同时引用 `${{ secrets.PROJECT_SECRET }}` 作为对照
  3. 提交并触发 workflow

预期结果:
  - 若环境级 secrets 不支持，系统应在解析阶段明确报错或给出警告
  - 不应静默降级为项目级 secrets（导致安全模型变化）
  - 项目级 secrets 应正常注入

验证点:
  - [负向] 不通过静默降级（ENV_SECRET 不应返回 PROJECT_SECRET 的值）
  - [正向] 系统对环境级 secrets 的缺失给出明确提示
  - [正向] 项目级 secrets 正常注入

清理:      重置 fixture 仓库
