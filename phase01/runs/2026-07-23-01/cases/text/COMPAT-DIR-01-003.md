用例 ID:   COMPAT-DIR-01-003
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-029
母意图:    —
标题:      .github/workflows 目录不应被识别且应给出迁移提示

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 在仓库中创建 `.github/workflows/test.yml` workflow 文件
  2. 提交并触发 push 事件
  3. 观察系统是否识别该 workflow

预期结果:
  - GitCode 行为：.github/workflows 下的 workflow 不应被识别
  - 系统应给出明确提示，说明 workflow 应放置在 .gitcode/workflows/ 目录下
  - 不应静默忽略导致用户误以为配置正确

验证点:
  - [负向] .github/workflows 下的 workflow 不应被触发
  - [正向] 系统给出迁移提示，说明正确的目录位置

清理:      无
