# 易用性 Intent 补充 · BLIND-06（Step Summary / Badge）

> 产出 Agent：usability（增量更新）
> Run：2026-07-21-02（delivered 状态，本次为增量补充，不修改历史结论）
> 来源：BLIND-06 `C-OBS-04 Step Summary / C-OBS-05 状态徽标 badge`——已有 USE-023 覆盖 error/warning 注解，但 step summary 写入可见性、badge SVG 无 intent。严重度：低。
> 纪律：ID 接续已有 USE-025，从 USE-026 起编；停在意图层，不写 GitCode 具体语法。

---

```
意图 ID:    INTENT-USE-026
维度标签:   [usability]
标题:       Step Summary（ATOMGIT_STEP_SUMMARY）写入后是否在运行详情页可见、超长内容是否截断及提示

风险点:     GitCode 规格声明支持通过环境文件写入 Step Summary（C-OBS-04），并承诺在运行详情页展示。迁移者从 GitHub 带来 `GITHUB_STEP_SUMMARY` 的使用习惯，核心诉求是「测试报告/构建摘要能在运行详情页结构化展示」。若写入后详情页无 Summary 区块、或 Markdown 未被渲染为富文本（仅原样打印），迁移者失去关键的可观测性入口。此外，文档未声明单 step summary 的大小上限与超长处理策略——若存在静默截断且无提示，用户会以为内容完整展示而误判（如测试报告被截断在「Failed: 0」处，实际后面还有失败项）。
预期系统行为: 写入 ATOMGIT_STEP_SUMMARY 的 Markdown 内容应在运行详情页有独立 Summary 区块，支持基本 Markdown 渲染（表格、标题、列表）；若内容超长被截断，应在截断处给出提示（如「内容已截断」）。
Oracle 来源: GitCode规格（C-OBS-04；runtime-environment-variables.md:186-200；workflow-commands.md:49-58）；GitHub行为（GITHUB_STEP_SUMMARY 在 workflow run summary page 展示并渲染 Markdown）

验证要点:
  - [正向] 正常长度的 Markdown summary（含表格、标题）在运行详情页可见且正确渲染。
  - [负向] 不应出现「写入了但详情页完全不可见」或「Markdown 被当纯文本原样展示」。
  - [非功能] 超长 summary 是否被截断、截断是否有提示；多 job 时 summary 聚合顺序是否符合「按完成时间展示」声明。

可理解性判据:
  - 可确定：运行详情页存在 summary 区块且内容非空；Markdown 表格有边框/标题有样式即判正确渲染（可确定判定）。
  - 超长截断提示应包含「截断」「超过」「省略」等关键字之一（可确定判定：grep 提示文本）。
  - 主观：summary 区块的醒目程度与导航便利性 → eval: llm_assisted。
优先级线索: BLIND-06（低严重度）；建议 P2。
来源输入:   inputs/gitcode-spec/syntax-reference/workflow-commands.md；runtime-environment-variables.md；view-run-results.md
```

```
意图 ID:    INTENT-USE-027
维度标签:   [usability]
标题:       Workflow 状态徽标 badge SVG 的可用性、分支过滤与状态同步及时性

风险点:     GitCode 文档声明支持将运行状态以 SVG 徽标嵌入 README（C-OBS-05），URL 格式为固定模板。迁移者从 GitHub 带来 badge 使用习惯，GitHub badge 支持按分支过滤（`?branch=main`）及事件过滤，且状态同步较及时。若 GitCode badge 不支持分支过滤，README 上的 badge 会展示全部分支的最新状态（如开发分支失败导致 main 的 badge 也显示失败），误导协作者。若状态同步延迟过长（如运行结束后数小时才刷新），badge 作为「项目健康度」入口的价值大打折扣。此外，文档未声明 `{workflow_name}` 的精确匹配规则（是文件名还是 workflow 的 `name` 字段），用户可能因名称不匹配拿到 404。
预期系统行为: badge URL 应返回有效 SVG 且状态与指定 workflow 最近运行一致；若支持分支过滤，参数格式应文档化；不支持则文档应给出替代方案或明确说明。状态变更后 badge 应在合理时限内刷新（建议不超过 5-10 分钟量级）。
Oracle 来源: GitCode规格（C-OBS-05；view-run-results.md:71-76）；GitHub行为（badge 支持 branch/event 参数，刷新及时）

验证要点:
  - [正向] badge URL 返回 SVG，图形/文本状态与最近运行结果一致。
  - [负向] 运行结果变更后 badge 不应长期显示旧状态（如失败运行后仍显示绿色通过徽标）。
  - [非功能] 是否支持按分支过滤；`{workflow_name}` 匹配规则（文件名 vs name 字段）的文档清晰度。

可理解性判据:
  - 可确定：SVG 内容包含与运行状态对应的颜色或文本（如绿/红、通过/失败），可确定判定。
  - 可确定：运行失败后 badge 在合理时限内（实测阈值 N 分钟，由门禁裁定）刷新为失败状态，可确定判定。
  - 主观：badge 嵌入文档的清晰度、分支过滤支持的「够用程度」→ eval: llm_assisted。
优先级线索: BLIND-06（低严重度）；建议 P2。
来源输入:   inputs/gitcode-spec/running-pipelines/view-run-results.md
```

---

*增量补充时间: 2026-07-21*
*对应盲区: BLIND-06 `C-OBS-04 Step Summary / C-OBS-05 badge`*
