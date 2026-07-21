用例 ID:   COMPAT-RUNSON-MIGR-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-036
母意图:    —
标题:      GitHub 单标签 runs-on 迁移到 GitCode 三段式的降级行为与报错质量

前置条件:
  - workflow 使用 GitHub 式单标签 runs-on: ubuntu-latest

操作步骤:
  1. 提交包含 runs-on: ubuntu-latest 的 workflow
  2. 观察平台解析与调度行为

预期结果:
  - 不应静默挂起或无提示失败
  - 应给出明确的格式错误或自动降级提示

验证点:
  - [负向] 不静默挂起超过 300 秒
  - [nonfunctional] 报错指明应使用三段式 [os, arch, flavor]

清理:      重置 fixture 仓库
