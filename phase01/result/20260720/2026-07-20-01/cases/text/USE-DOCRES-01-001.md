用例 ID:   USE-DOCRES-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-007
标题:      文档中残留 GitHub 措辞（GITHUB_*）的核对与修正

前置条件:
  - 可访问 `gitcode-spec/` 下所有 .md 文件全文

操作步骤:
  1. 全文搜索 `gitcode-spec/` 下所有 .md 文件，grep 匹配 `GITHUB_`
  2. 对每个匹配实例，判断是否出现在「与 GitHub 对比」章节且明确标注为「GitHub 特有」
  3. 特别检查 `action-development/runtime-environment-variables.md` 是否残留 `GITHUB_ACTION_PATH` / `GITHUB_WORKSPACE`

预期结果:
  - GitCode 官方文档中不应出现 GitHub-only 的环境变量名（如 GITHUB_ACTION_PATH、GITHUB_WORKSPACE）
  - 若出现，必须位于明确的「与 GitHub 对比」章节，且标注为「GitHub 特有，GitCode 不对应」
  - 若某页面同时描述 ATOMGIT 和 GITHUB 变量且未区分，即视为文档缺陷

验证点:
  - [正-非功能] grep `GITHUB_` 在非对比上下文中结果应为零
  - [正-非功能] 若存在残留，每条均应在对比章节且有标注说明

清理:      none
