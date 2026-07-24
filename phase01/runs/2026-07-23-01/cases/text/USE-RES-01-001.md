用例 ID:   USE-RES-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-012
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      runtime-environment-variables.md 中不应出现未标注的 GitHub 专属变量名

前置条件:
  - 文档版本为 2026-07-20 抓取版本

操作步骤:
  1. 对 runtime-environment-variables.md 全文进行字符串扫描

预期结果:
  独立出现的环境变量示例均使用 ATOMGIT_ 前缀；未标注为 GitHub 对照的 GITHUB_ 残留数量为 0

验证点:
  - [正向] 所有独立环境变量示例使用 ATOMGIT_ 前缀
  - [负向] 正文中不应出现未标注为 GitHub 对照的 GITHUB_ACTION_PATH、GITHUB_ENV 等残留措辞

清理:      无

