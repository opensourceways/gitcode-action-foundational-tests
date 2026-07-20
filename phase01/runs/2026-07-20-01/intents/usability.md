# Usability Test Intents

> Agent: usability | Run: 2026-07-20-01 | Date: 2026-07-20
> 
> 输入快照:
> - `phase01/inputs/gitcode-spec/` (50 页, 2026-07-20)
> - `phase01/inputs/github-reference/` (12 页, 2026-07-20)
> - `phase01/inputs/existing-cases/cases.md` (631 条, 2026-07-20)
> - `phase01/baseline/risk-register.md` (RISK-USE-01)
> - `phase01/baseline/parity-matrix.md`
> - `phase01/baseline/quality-gate.md`
>
> 退化声明:
> - `inputs/workflow-samples/` 缺失: 迁移摩擦 intent 基于 spec diff 分析而非真实 workflow 搬运, 准确性打折。
> - `inputs/business-context/` 缺失: 无真实迁移规模/改造点/历史踩坑记录, 场景选择偏通用, 可能遗漏特定业务路径的摩擦。
>
> 现有用例去重说明:
> - 已审查 `cases.md` 631 条用例。现有用例聚焦**功能行为验证** (语法合法→跑绿; 字段取值→匹配; 事件触发→命中)。
> - 本批 intent 聚焦**体验层**: 报错是否可理解、文档是否一致、迁移是否顺畅、调试是否高效。
> - 部分 intent 与现有用例有场景重叠 (如同一 YAML 错误), 但关注维度不同: 现有用例验证「行为对不对」, 本批 intent 验证「报错能不能让人自己修好」。

---

## A. 错误信息质量 — YAML 解析与静态校验

---

意图 ID:    INTENT-USE-001
维度标签:   [usability]
标题:       必填字段缺失时的错误信息可诊断性

风险点:     YAML 解析阶段, 若 workflow 缺少必填字段 (如 `on:` 或 `jobs:`), 平台可能只报 "invalid workflow syntax" 而不指明缺失哪个字段、在第几行。新用户无从修起。
预期系统行为: 错误信息必须包含:
              (1) 缺失的字段名 (如 `on` 或 `jobs`);
              (2) 出错文件路径 (如 `.gitcode/workflows/ci.yml`);
              (3) 出错行号或 YAML 路径 (如 `line 3` 或 `root > missing 'on'`);
              (4) 该字段是否为必填的说明 (如 `'on' is required`).
Oracle 来源: 启发式可诊断性准则 (testing-focus.md §1: "错在第几行、给不给可操作提示"); GitHub Actions 实际行为作参照。

验证要点:
  - [正向] 提交一个缺少 `on:` 的 workflow YAML, 系统报错且消息包含缺失字段名、文件路径、大致位置。
  - [正向] 提交一个缺少 `jobs:` 的 workflow YAML, 系统报错且消息包含缺失字段名、文件路径、大致位置。
  - [非功能] 一个不熟悉 GitCode 的开发者应能在 5 分钟内根据该报错自行修复。

可理解性判据:
  - 确定性部分: 消息是否包含上述 4 项信息 (逐项可判定)。
  - `eval: llm_assisted` 部分: 若信息不全, 需 LLM 评估「新手能否仅凭该消息定位并修复」, 评判标准: 0=完全无法修复, 1=需多次试错, 2=一次试对。

优先级线索: P1 (关联 RISK-USE-01: 迁移报错不指明差异; 此处扩展为「任意无效定义报错不指明缺失内容」)
破坏级别:   none
来源输入:   `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §基本结构字段; `testing-focus.md` §1

---

意图 ID:    INTENT-USE-002
维度标签:   [usability]
标题:       字段类型错误时的错误信息可诊断性

风险点:     当 YAML 中某字段期望 string 但给了 list (或反之) 时, 平台可能报泛化的类型错误 (如 "type mismatch") 而不指明哪个字段、期望什么类型、实际收到什么类型。
预期系统行为: 类型错误消息应包含:
              (1) 字段路径 (如 `jobs.build.runs-on`);
              (2) 期望类型 (如 `expected: string`);
              (3) 实际收到类型 (如 `got: list`);
              (4) 文件与行号。
Oracle 来源: 启发式可诊断性准则; GitHub Actions 实际错误信息作参照。

验证要点:
  - [正向] 将 `runs-on` 写成 string 而非 list (如 `runs-on: ubuntu-latest` — 合法 GitHub 写法但不合法于 GitCode 三段式), 验证错误消息指出 `runs-on` 字段类型不对。
  - [正向] 将 `env` 写成 string 而非 map (如 `env: "foo"`), 验证错误消息明确指出类型错误。

可理解性判据:
  - 确定性: 是否包含字段路径 + 期望类型 + 实际类型 + 行号 (逐项可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001 三级评判标准。

优先级线索: P1 (关联 RISK-USE-01)
破坏级别:   none
来源输入:   `testing-focus.md` §1; `gitcode-spec/writing-pipelines/workflow-file-location-structure.md`

---

意图 ID:    INTENT-USE-003
维度标签:   [usability]
标题:       未知字段/不支持属性时的错误信息可诊断性

风险点:     GitHub workflow 直接搬到 GitCode 时, 可能包含 GitCode 不支持的字段 (如 `container.credentials`、GitHub 特有的 `environment` 语法等)。若平台**静默忽略**未知字段, 用户不会发现配置未生效; 若平台**报错**, 消息是否点明「该字段 GitCode 不支持」决定了用户能否定位根因。
预期系统行为:
             若平台选择报错: 消息应明确指出字段不被支持、给出字段路径、建议查阅 GitCode 文档。
             若平台选择静默忽略: 应将忽略的字段列表写入运行日志 `warning` 级别, 不应完全无声。
Oracle 来源: COMPAT-NOTES.md §6/§10 (权限命名差异、内置 action 差异); 现有案例 TC-010 (`environment` 字段报 "unknown property") 作已知基线。

验证要点:
  - [正向] 在 YAML 中添加 GitHub 支持但 GitCode 文档未列的字段 (如 `jobs.<id>.container.credentials`), 观察是报错还是静默忽略。
  - [负向] 若静默忽略: 不应没有任何 warning 级别的日志提示; 用户不应在 run 成功后才从行为差异中反向发现字段未生效。
  - [非功能] 若报错, 消息应含字段路径 + 是否属于 "GitCode vs GitHub 差异" 的提示。

可理解性判据:
  - 确定性: 是否有任何可见提示 (错误/警告) 表明该字段未被处理; 消息是否指明字段路径。
  - `eval: llm_assisted`: 若报错或 warning 存在, 评估消息是否能让 GitHub 迁移者意识到这是 GitCode 差异 (而非 YAML 拼写错误)。

优先级线索: P1 (关联 RISK-USE-01)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §6/§8/§10; 现有案例 TC-010

---

意图 ID:    INTENT-USE-004
维度标签:   [usability]
标题:       触发器 types 取值无效时的错误信息可诊断性

风险点:     GitCode 的 `pull_request.types` 取值为 `[merge, open, reopen, update]` (COMPAT-NOTES.md §5), 与 GitHub 的 `[opened, synchronize, reopened, ...]` 命名不同。直接搬 GitHub workflow 时配了 `types: [opened, synchronize]`, 平台如何处理? 报错是否指出合法值列表?
预期系统行为: 当 `pull_request.types` 含非法值时, 错误信息应包含:
              (1) 无效值的名称 (如 `'opened' is not a valid type`);
              (2) 合法值列表 (如 `valid types: [merge, open, reopen, update]`);
              (3) 文件位置。
Oracle 来源: COMPAT-NOTES.md §5 (types 差异); GitHub Actions 对无效 types 的报错行为作参照。

验证要点:
  - [正向] 配置 `pull_request.types: [opened]` (GitHub 命名), 验证报错且指出合法值。
  - [正向] 配置 `pull_request.types: [synchronize]` (GitHub 命名), 同上。
  - [正向] 配置 `pull_request.types: [invalid_value]`, 验证任一无效值即报错。

可理解性判据:
  - 确定性: 是否包含无效值 + 合法值列表 + 文件位置 (逐项可判定)。
  - `eval: llm_assisted`: 若缺少合法值列表, 评判用户能否从文档自行找到 (0=无法, 1=需搜索, 2=错误消息直接给出)。

优先级线索: P1 (关联 RISK-USE-01)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §5; `gitcode-spec/writing-pipelines/configure-triggers.md`

---

意图 ID:    INTENT-USE-005
维度标签:   [usability]
标题:       表达式语法差异 (状态函数括号) 的错误信息可诊断性

风险点:     GitCode 的状态检查写 `success`/`failed`(无括号), GitHub 写 `success()`/`failure()`(带括号) (COMPAT-NOTES.md §3)。直接搬 GitHub workflow 时 `if: ${{ failure() }}` 可能报语法错误, 但消息能否让用户意识到「是 GitCode 不需要括号」?
预期系统行为: 当表达式中使用了 GitHub 风格的状态函数语法 (如 `success()`, `failure()`, `cancelled()`, `always()`), 错误信息应:
              (1) 指出表达式语法错误的位置;
              (2) 提示 GitCode 状态检查不需要括号 (如 `use 'success' instead of 'success()'`)。

Oracle 来源: COMPAT-NOTES.md §3; `gitcode-spec/syntax-reference/expressions.md` §3.3

验证要点:
  - [正向] 配置 `if: ${{ failure() }}`, 验证报错且消息提示括号多余。
  - [正向] 配置 `if: ${{ always() }}`, 同上。
  - [正向] 配置 `if: ${{ success() }}`, 同上。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否含表达式位置。
  - `eval: llm_assisted`: 消息是否足以让 GitHub 迁移者意识到「GitCode 不需要括号」这一差异 (0=看不出, 1=需查文档, 2=消息直接说明)。

优先级线索: P1 (关联 RISK-USE-01)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §3; `gitcode-spec/syntax-reference/expressions.md`; `github-reference/reference/expressions.md`

---

意图 ID:    INTENT-USE-006
维度标签:   [usability]
标题:       上下文对象命名差异 (`github.*` vs `atomgit.*`) 的错误信息可诊断性

风险点:     GitHub workflow 遍地 `${{ github.ref }}` / `${{ github.sha }}` / `${{ github.event_name }}`。直接搬到 GitCode 会因为 `github` 上下文不存在而报错, 但错误消息能否明确告诉用户「换个名字就行」, 还是只报 "unknown context 'github'"?
预期系统行为: 当使用 `${{ github.* }}` 时, 错误信息应:
              (1) 指出 `github` 上下文不被识别;
              (2) 明确提示 GitCode 使用 `atomgit` 上下文替代 — 这是迁移摩擦第一关, 错误消息质量决定用户是 1 分钟修好还是花 30 分钟搜索。
Oracle 来源: COMPAT-NOTES.md §2; `gitcode-spec/syntax-reference/context.md`

验证要点:
  - [正向] 在 workflow 中使用 `${{ github.ref }}`, 验证报错且提示应使用 `atomgit.ref`。
  - [正向] 使用 `${{ github.event_name }}`, 同上。
  - [正向] 使用 `${{ github.workspace }}`, 同上。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否含 `github` 不被识别。
  - `eval: llm_assisted`: 消息是否暗示用户应将 `github` 替换为 `atomgit` (0=无提示, 1=需查文档, 2=消息直接说)。

优先级线索: P1 (关联 RISK-USE-01) — 这是迁移摩擦头号触点
破坏级别:   none
来源输入:   COMPAT-NOTES.md §2; `gitcode-spec/syntax-reference/context.md`; `github-reference/reference/contexts.md`

---

## B. 文档一致性

---

意图 ID:    INTENT-USE-007
维度标签:   [usability]
标题:       文档中残留 GitHub 措辞的核对与修正

风险点:     COMPAT-NOTES.md §2 指出 `runtime-environment-variables.md` 描述文案中夹带 `GITHUB_ACTION_PATH` 等 GitHub 残留措辞。用户在 GitCode 文档中看到 `GITHUB_*` 会困惑「到底该用哪个」, 降低文档可信度。
预期系统行为: GitCode 官方文档中不应出现 GitHub-only 的环境变量名 (如 `GITHUB_ACTION_PATH`、`GITHUB_WORKSPACE`) 除非在明确的「与 GitHub 对比」章节且标注为「GitHub 特有, GitCode 不对应」。
Oracle 来源: COMPAT-NOTES.md §2; `gitcode-spec/action-development/runtime-environment-variables.md`

验证要点:
  - [正向] 全文搜索 `gitcode-spec/` 下所有 `.md` 文件, 列出仍含 `GITHUB_*` (非对比/非标注上下文) 的实例。
  - [正向] 逐条验证: 若某页面同时描述 ATOMGIT 和 GITHUB 变量且未区分, 即视为文档缺陷。

可理解性判据:
  - 确定性: `grep` 搜索可确定性判定是否存在残留措辞。
  - 无需 llm_assisted。

优先级线索: P2 (文档缺陷, 不阻塞上线但影响迁移体验)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §2; `gitcode-spec/action-development/runtime-environment-variables.md`

---

意图 ID:    INTENT-USE-008
维度标签:   [usability]
标题:       文档声明的 `environment` 绑定语法与实际校验行为的一致性

风险点:     现有案例 TC-010 显示 `environment` 字段被平台报 "unknown property", 但文档 (`using-variables-secrets.md`) 描述了环境级 secret 审批功能。如果平台不支持文档所述语法, 用户按文档配置后报错会非常困惑: 「你文档说可以, 为什么报错?」
预期系统行为: 文档声明的能力应有对应的合法 YAML 语法, 且该语法被平台接受 (不报 "unknown property")。若能力尚未实现, 文档必须标注 "规划中" 或 "暂不支持"。
Oracle 来源: 现有案例 TC-010 (FAIL: `environment` 报 unknown property); `gitcode-spec/security-permissions/using-secrets.md`

验证要点:
  - [正向] 按文档示例配置 `jobs.<id>.environment`, 验证平台接受该字段 (不报 "unknown property")。
  - [负向] 若平台仍不接受: 文档必须在该处明确标注能力状态。

可理解性判据:
  - 确定性: 平台是否接受文档示例中的 `environment` 字段 (可观测)。
  - `eval: llm_assisted`: 若存在文档-行为不一致, 评估用户按文档操作后的困惑程度。

优先级线索: P1 (文档承诺与实际行为不符, 直接影响用户信任)
破坏级别:   none
来源输入:   现有案例 TC-010; `gitcode-spec/security-permissions/using-secrets.md`

---

意图 ID:    INTENT-USE-009
维度标签:   [usability]
标题:       文档声明的 `runner.os` / `runner.arch` 返回值与平台实际返回值的一致性

风险点:     文档 (`context.md` §2.4) 声明 `runner.os` 返回 `Linux`/`Windows`/`macOS`, `runner.arch` 返回 `X64`/`ARM`/`ARM64`。但现有案例 TC-023 显示平台实际返回了 `linux`(全小写), TC-095 显示返回 `x86_64`(而非 `X64`)。用户按文档写 `if: ${{ runner.os == 'Linux' }}` 可能永远不匹配, 且无报错, 极难排查。
预期系统行为: 文档声明的取值必须与平台实际返回值一致。若不改变平台行为, 则文档必须更新为实际取值 (如 `runner.os: linux`, `runner.arch: x86_64`)。
Oracle 来源: 现有案例 TC-023 (FAIL), TC-095 (FAIL); `gitcode-spec/syntax-reference/context.md` §2.4

验证要点:
  - [正向] 在 workflow 中输出 `runner.os` 值, 与文档比对。
  - [正向] 在 workflow 中输出 `runner.arch` 值, 与文档比对。
  - [负向] 文档与平台返回值不应存在大小写/命名差异。

可理解性判据:
  - 确定性: 实际返回值与文档声明值是否一致 (字符串比对可确定性判定)。
  - 无需 llm_assisted。

优先级线索: P1 (文档-行为不一致且属静默错误, 用户可能长时间无法发现根因)
破坏级别:   none
来源输入:   现有案例 TC-023, TC-095; `gitcode-spec/syntax-reference/context.md`

---

## C. 调试体验与可观测性

---

意图 ID:    INTENT-USE-010
维度标签:   [usability]
标题:       日志中 `::group::` / `::endgroup::` workflow 命令的实际支持情况

风险点:     GitHub Actions 支持 `::group::{title}` / `::endgroup::` 折叠分组 (workflow-commands.md), 极大改善长日志可读性。GitCode 的 workflow-commands.md 文档**完全没有提及** `::group::` / `::endgroup::` / `::error::` / `::warning::` / `::debug::` / `::notice::` 等日志格式命令, 但日志界面有 "折叠" 概念 (view-job-logs.md)。用户从 GitHub 搬来的 `echo "::group::Build"` 是否生效? 不生效的话是否静默失败?
预期系统行为:
             - 若 GitCode 支持 `::group::`/`::endgroup::`: 日志应有可视化折叠效果。
             - 若 GitCode 不支持: 文档必须明确说明; 不支持的 workflow 命令不应导致 step 失败, 但宜在日志中无影响地原样输出。
Oracle 来源: `github-reference/reference/workflow-commands.md` (GitHub 行为); `gitcode-spec/syntax-reference/workflow-commands.md` (GitCode 文档 — 注意未列 `::group::`)

验证要点:
  - [正向] 在 step 中使用 `echo "::group::My Group"` ... `echo "::endgroup::"`, 观察日志是否有折叠效果。
  - [正向] 使用 `echo "::error file=app.js,line=10::Something wrong"`, 观察是否生成 annotation。
  - [正向] 使用 `echo "::warning::Some warning"`, 同上。
  - [负向] 若不支持: 不应导致 step 非零退出或 workflow 失败。

可理解性判据:
  - 确定性: `::group::` 是否产生折叠效果 (可屏幕截图判定); step 是否因不识别而失败 (可判定)。
  - 无需 llm_assisted。

优先级线索: P1 (日志可读性直接影响调试效率; 若静默不支持则用户无从知道为什么不折叠)
破坏级别:   none
来源输入:   `testing-focus.md` §9; `github-reference/reference/workflow-commands.md`; `gitcode-spec/syntax-reference/workflow-commands.md`; `gitcode-spec/running-pipelines/view-job-logs.md`

---

意图 ID:    INTENT-USE-011
维度标签:   [usability]
标题:       运行状态机的完整性与可观察性

风险点:     testing-focus.md §9 定义了 CI/CD 的 5 态: queued → in_progress → completed (success/failure/cancelled/skipped)。用户需要知道自己的 workflow 是否在排队、为何被跳过、为何被取消。若状态机不完整或转换不透明, 用户无法判断「是 bug 还是等一会就好」。
预期系统行为:
             - Actions 标签页应显示清晰的运行状态: queued / in_progress / success / failure / cancelled / skipped.
             - queued 状态应显示排队位置或预计等待时间 (若有 concurrency 排队)。
             - cancelled 状态应显示取消原因 (手动取消 vs 被抢占 vs fail_fast 级联)。
             - skipped job 应有可见的跳过原因。
Oracle 来源: `testing-focus.md` §9; `gitcode-spec/running-pipelines/view-run-results.md`

验证要点:
  - [正向] 触发一个需排队的 workflow (concurrency queue), 观察 queued 状态是否可见及排队信息是否展示。
  - [正向] 手动取消一个正在运行的 workflow, 观察 cancelled 状态及取消原因展示。
  - [正向] 配置 fail_fast 场景, 观察被跳过的 stage/job 是否有 "skipped: upstream job failed" 类的说明。

可理解性判据:
  - 确定性: 状态标签是否展示 (可截图判定); 取消/跳过原因文本是否存在 (可判定)。
  - `eval: llm_assisted`: 若原因文本存在, 评估其是否足够具体 (如 "cancelled by user @username" vs 仅 "cancelled")。

优先级线索: P2 (体验改善, 有 workaround: 去查配置和日志)
破坏级别:   none
来源输入:   `testing-focus.md` §9; `gitcode-spec/running-pipelines/view-run-results.md`

---

意图 ID:    INTENT-USE-012
维度标签:   [usability]
标题:       日志中 `ATOMGIT_*` 系统变量的注入完整性

风险点:     现有案例 TC-206 报告 `ATOMGIT_REPOSITORY_OWNER` 未注入 Runner。日志中 `ATOMGIT_*` 系统变量是用户调试的重要上下文 (如确认触发人、触发 SHA、仓库名), 缺失会导致用户在调试时多一步「我需要确认环境对不对」的摩擦。
预期系统行为: 文档 `view-job-logs.md` 列出的所有 `ATOMGIT_*` 系统变量 (共 8 个: `ATOMGIT_REPOSITORY`, `ATOMGIT_EVENT_NAME`, `ATOMGIT_REF`, `ATOMGIT_SHA`, `ATOMGIT_ACTOR`, `ATOMGIT_TOKEN`, `ATOMGIT_RUN_ID`, `ATOMGIT_RUN_NUMBER`) 应在 Runner 环境中有效注入且值正确。
Oracle 来源: `gitcode-spec/running-pipelines/view-job-logs.md`; 现有案例 TC-206 (ATOMGIT_REPOSITORY_OWNER 未注入)

验证要点:
  - [正向] 在 step 中 `echo` 所有 8 个 `ATOMGIT_*` 变量, 验证每个都有非空正确值。
  - [正向] 特别验证 `ATOMGIT_REPOSITORY` 包含正确的 owner/repo 格式; `ATOMGIT_ACTOR` 匹配触发用户。

可理解性判据:
  - 确定性: 每个变量是否非空且值合理 (可 shell 脚本断言)。
  - 无需 llm_assisted。

优先级线索: P1 (文档列了但缺失 → 文档-行为不一致; 影响调试效率)
破坏级别:   none
来源输入:   现有案例 TC-206; `gitcode-spec/running-pipelines/view-job-logs.md`

---

意图 ID:    INTENT-USE-013
维度标签:   [usability]
标题:       运行详情页 `post` 阶段的展示与文档一致性

风险点:     post 是 GitCode 特有的后处理阶段 (workflow-file-location-structure.md)。文档称 post 默认 `run_always: true`。运行详情页是否确实将 post 阶段与主 stages 区分展示? 用户体验上, 如果 post 和正常 stage 混在一起且无标注, 用户会困惑「这个 deploy notification 为啥跑在 build 前面?」
预期系统行为:
             - 运行详情页 post 阶段应单独展示, 标注 "post" 或 "后处理"。
             - post 阶段失败不应标记主 workflow 为 failure (若 post 仅做通知清理, `run_always` 独立判定)。
Oracle 来源: `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §post; `gitcode-spec/running-pipelines/view-run-results.md`

验证要点:
  - [正向] 配置带 post 的 workflow, 故意主流程成功、post 失败, 观察运行详情页如何呈现 post 状态。
  - [非功能] post 阶段的标识 (名称/标签) 应能让用户一眼看出这是「后处理」而非主流程的 stage。

可理解性判据:
  - 确定性: post 是否有独立展示区域; 标注文字是否含 "post"/"后处理" (可判定)。
  - `eval: llm_assisted`: UI 呈现是否直观 (需截图评判)。

优先级线索: P2 (体验改善)
破坏级别:   none
来源输入:   `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §post; `gitcode-spec/running-pipelines/view-run-results.md`

---

## D. 迁移摩擦

---

意图 ID:    INTENT-USE-014
维度标签:   [usability, compatibility]
标题:       直接搬运 `.github/workflows/ci.yml` 到 `.gitcode/workflows/` 后的开箱报错路径

风险点:     这是迁移摩擦端到端主干场景。用户把 GitHub workflow 文件直接复制到 `.gitcode/workflows/` 目录下, 不改任何内容。按照已知差异清单 (COMPAT-NOTES.md), 至少会命中以下差异: (1) 目录名不对; (2) `github.*` 上下文; (3) `runs-on: ubuntu-latest`; (4) `permissions` 命名; (5) `uses: actions/checkout@v4`; (6) `success()`/`failure()` 函数语法; (7) `pull_request.types` 命名。问题是: 用户会收到**一个报错**还是**一串报错**? 如果是多个, 能否一次性扫完所有问题而不是修一个再撞一个?
预期系统行为: 平台应一次性报告发现的所有语法/语义问题 (批量校验), 而不是碰到第一个错误就停止 (逐错修复导致迁移变成多轮「改→提交→报错→改→提交→报错」的挫败循环)。
Oracle 来源: COMPAT-NOTES.md (全部差异点); `testing-focus.md` §11

验证要点:
  - [正向] 将一个标准 GitHub workflow (含 `on.push.branches`, `jobs.build.runs-on: ubuntu-latest`, `uses: actions/checkout@v4`, `if: failure()`, `permissions: contents: read`) 原样放入 `.gitcode/workflows/`, 触发 push, 观察报错列表。
  - [非功能] 应尽量在一次提交后暴露所有语法/语义问题; 修改一轮后 (至少修正 `github`→`atomgit` + `runs-on` + `permissions` 命名) 第二次提交不应再报同类语法错误。

可理解性判据:
  - 确定性: 是否一次性暴露多个错误 (可数报错条数)。
  - `eval: llm_assisted`: 每个报错消息是否能让开发者定位到对应的迁移改造点 (0=无法定位, 1=需查 diff 文档, 2=消息直接指出差异和修复方法)。

优先级线索: P1 (关联 RISK-USE-01 — 迁移摩擦头号场景)
破坏级别:   none
来源输入:   COMPAT-NOTES.md (全部差异点); `testing-focus.md` §11; `github-reference/reference/workflow-syntax.md`
退化说明:   `workflow-samples/` 缺失, 使用虚构的「典型 GitHub CI workflow」替代; 场景覆盖可能遗漏非标准用法。

---

意图 ID:    INTENT-USE-015
维度标签:   [usability, compatibility]
标题:       `runs-on` 使用 GitHub 风格标签时的错误信息质量与迁移指引

风险点:     GitHub 用 `runs-on: ubuntu-latest`, GitCode 用三段式 `runs-on: [{os-version},{arch},{flavor}]` (COMPAT-NOTES.md §7)。直接搬来的 GitHub workflow 中 `runs-on: ubuntu-latest` 被 GitCode 解析时, 报错是否说清楚「GitCode 标签格式是三段的, 不是单个字符串」?
预期系统行为: 当 `runs-on` 值为 GitHub 风格 (如 `ubuntu-latest`, `windows-latest`, `macos-latest`) 时, 错误信息应:
              (1) 指出标签格式不匹配;
              (2) 给出 GitCode 可用标签示例 (如 `{ubuntu-24,x64,small}` 或 `default`);
              (3) 提供文档链接或章节引用。
Oracle 来源: COMPAT-NOTES.md §7; `gitcode-spec/runner-management/selecting-runner-labels.md`

验证要点:
  - [正向] 配置 `runs-on: ubuntu-latest`, 验证报错且消息指出 GitCode 三标签格式。
  - [正向] 配置 `runs-on: [ubuntu-latest]` (数组但单标签), 同上。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否含 'ubuntu-latest' 和格式说明 (逐项可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001 三级评判。

优先级线索: P1 (关联 RISK-USE-01 — 迁移摩擦高发点)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §7; `gitcode-spec/runner-management/selecting-runner-labels.md`

---

意图 ID:    INTENT-USE-016
维度标签:   [usability, compatibility]
标题:       `permissions` 使用 GitHub 命名体系时的错误信息质量

风险点:     GitHub `permissions: { contents: read, pull-requests: write }` 在 GitCode 下完全不通 (COMPAT-NOTES.md §6: GitCode 用 `project`/`pr`/`repository` 等不同命名)。若平台将不识别的权限名静默忽略, 可能导致「以为自己设了只读但实际上权限没生效」的安全/行为问题。
预期系统行为: 当 `permissions` 中使用 GitCode 不识别的权限项 (如 `contents`, `pull-requests`, `actions`, `packages`, `deployments`) 时, 平台应:
              (1) 报错或至少 warning (不可静默忽略);
              (2) 指出不识别的权限项名称;
              (3) 给出 GitCode 可用权限项列表 (project/pr/issue/note/repository/hook)。
Oracle 来源: COMPAT-NOTES.md §6; `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §permissions

验证要点:
  - [正向] 配置 `permissions: { contents: read }` (GitHub 命名), 验证是否报错/warning。
  - [正向] 配置 `permissions: { pull-requests: write }`, 同上。
  - [负向] 若静默忽略: 验证实际权限可能仍是默认值 (危险)。

可理解性判据:
  - 确定性: 报错/warning 是否发生; 不识别项是否被点明 (可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001。

优先级线索: P0 (静默忽略权限差异 = 安全/行为风险; 涉及 RISK-USE-01 叠加 RISK-COMPAT-01)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §6; `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §permissions

---

意图 ID:    INTENT-USE-017
维度标签:   [usability, compatibility]
标题:       `uses: actions/checkout@v4` 等带 owner+版本的内置 action 引用在 GitCode 下的行为与报错

风险点:     GitCode 内置 action 用无 owner 短名 (`checkout`, `setup-node`, 等, COMPAT-NOTES.md §10)。GitHub workflow 写 `uses: actions/checkout@v4` 时, GitCode 如何解析? 是报 "action 'actions/checkout' not found" 还是尝试去拉 `actions/checkout` 仓库而超时? 错误消息是否提示 GitCode 等价写法 (`uses: checkout`)?
预期系统行为: 当 `uses` 引用包含 `owner/repo@ref` 格式的非内置 action 时, 若它对应 GitCode 内置 action, 错误消息应提示用短名替代 (如 `use 'checkout' instead of 'actions/checkout@v4'`)。

Oracle 来源: COMPAT-NOTES.md §10; `gitcode-spec/writing-pipelines/using-actions.md`; `gitcode-spec/action-development/plugin-development-guide.md`

验证要点:
  - [正向] 配置 `uses: actions/checkout@v4`, 观察报错内容和 step 状态。
  - [正向] 配置 `uses: actions/setup-node@v4`, 同上。
  - [正向] 配置 `uses: actions/cache@v4`, 同上。

可理解性判据:
  - 确定性: 报错是否发生; 是否提示短名替代。
  - `eval: llm_assisted`: 同 INTENT-USE-001。

优先级线索: P1 (关联 RISK-USE-01; `checkout` 几乎是每个 workflow 第一步)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §10; `gitcode-spec/writing-pipelines/using-actions.md`

---

意图 ID:    INTENT-USE-018
维度标签:   [usability, compatibility]
标题:       `workflow_dispatch.inputs` 使用 GitHub 支持的非 string 类型时的行为与报错

风险点:     GitCode `inputs` 仅支持 `string` 类型 (COMPAT-NOTES.md §9), GitHub 支持 `boolean`/`choice`/`number`/`environment`。直接搬 GitHub workflow 时写了 `type: boolean`, 平台如何处理? 是报错还是把 boolean 当 string 静默处理? 若静默处理, `default: true` 变成 `default: "true"` 字符串, 表达式 `${{ inputs.dry_run == true }}` 因类型不匹配静默失败。
预期系统行为: 当 `inputs` 中使用了 `string` 以外的 type 时, 平台应明确报错, 指出不支持的类型及 GitCode 仅支持 `string`。
Oracle 来源: COMPAT-NOTES.md §9; `gitcode-spec/writing-pipelines/configure-triggers.md`

验证要点:
  - [正向] 配置 `workflow_dispatch.inputs.dry_run.type: boolean`, 验证报错且提示仅支持 string。
  - [正向] 配置 `type: number`, 同上。
  - [正向] 配置 `type: choice`, 同上。

可理解性判据:
  - 确定性: 报错是否发生; 是否提示仅支持 string (可判定)。
  - `eval: llm_assisted`: 同 INTENT-USE-001。

优先级线索: P1 (关联 RISK-USE-01; 静默类型转换可能引入难以排查的逻辑 bug)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §9; `gitcode-spec/writing-pipelines/configure-triggers.md`

---

意图 ID:    INTENT-USE-019
维度标签:   [usability]
标题:       迁移清单文档的完整性与可操作性

风险点:     COMPAT-NOTES.md 列出了全部已知差异点 (11 大类约 30+ 条), 但这属于 agent 分析产物, 用户看不到。面向用户的「从 GitHub 迁移到 GitCode」指南是否存在? 是否覆盖了上下文命名、permissions 命名、runs-on 格式、types 命名、表达式语法、inputs 类型限制、内置 action 引用这 7 个「不改就报错」的差异点?
预期系统行为: 存在一份从 GitHub Actions 迁移到 GitCode Action 的官方指南, 且至少覆盖上述 7 个「不改就报错」的差异点, 每个差异点配有: 差异说明 + GitHub 写法 + GitCode 写法 + 报错现象 (若不改)。
Oracle 来源: COMPAT-NOTES.md (差异总清单); 最佳实践: 迁移指南应覆盖所有阻断性差异。

验证要点:
  - [正向] 搜索 GitCode 官方文档中是否存在 "Migrate from GitHub Actions" / "从 GitHub 迁移" 等关键词的页面。
  - [正向] 逐条核对该迁移指南是否覆盖上述 7 个阻断性差异点。
  - [非功能] 每个差异点的改写示例应可直接复制使用。

可理解性判据:
  - 确定性: 迁移指南是否存在; 覆盖了几个阻断性差异点 (可数)。
  - `eval: llm_assisted`: 若存在, 评估指南的操作性 (代码示例是否可复制; 说明是否够具体; 0=不可操作, 1=部分可操作, 2=完整可操作)。

优先级线索: P1 (关联 RISK-USE-01: 迁移报错不指明 GitCode 差异 → 缺少迁移指南是同一问题的另一面)
破坏级别:   none
来源输入:   COMPAT-NOTES.md; 所有 gitcode-spec 文档; `testing-focus.md` §11
退化说明:   `business-context/` 缺失, 无法评估迁移指南是否覆盖实际迁移规模中的常见场景。

---

## E. 重新运行体验

---

意图 ID:    INTENT-USE-020
维度标签:   [usability]
标题:       Re-run failed jobs 后成功 job 的结果和日志保留与展示

风险点:     `rerun-failed-jobs.md` 声称 "成功 job 的日志和结果被保留在新运行的详情页中, 状态徽标显示'已缓存'或'已通过', 可展开查看原始日志"。若此承诺不兑现, 用户重跑失败 job 后就丢失了成功 job 的日志, 导致「想看成功 job 的日志确认环境状态」时必须回到原始 run, 割裂调试流程。
预期系统行为:
             - Re-run failed jobs 后, 新 run 的详情页中应保留成功 job 的结果, 标注 "cached" / "已缓存" / "passed" / "已通过"。
             - 成功 job 的原始日志仍可展开查看。
             - 原始 run 的日志不应被清除或覆盖。

Oracle 来源: `gitcode-spec/running-pipelines/rerun-failed-jobs.md` §常见问题 Q&A

验证要点:
  - [正向] 配置一个多 job workflow (其中 job A 成功, job B 失败), re-run failed jobs, 验证新 run 中 job A 显示 cached 且日志可查。
  - [正向] 验证原始 run 的日志仍然完整。
  - [负向] 成功 job 不应被隐式重新执行 (即不应消耗额外 Runner 资源)。

可理解性判据:
  - 确定性: cached 状态是否显示; 日志是否可展开 (可屏幕截图判定)。
  - 无需 llm_assisted。

优先级线索: P1 (文档承诺的核心功能, 调试流程的关键环节)
破坏级别:   none
来源输入:   `gitcode-spec/running-pipelines/rerun-failed-jobs.md`

---

意图 ID:    INTENT-USE-021
维度标签:   [usability]
标题:       重新运行的限制条件 (3次/6小时/原始配置) 的用户可见性与反馈

风险点:     `rerun-failed-jobs.md` 声明了 3 个限制: 最多重试 3 次; 超过 6 小时的运行不可重新运行; 使用原始 commit 配置。若用户不知道这些限制:
             - 第 4 次点 Re-run 按钮灰掉/无反应 → 困惑 "为什么不能重跑了?"
             - 6 小时运行结束后 Re-run 按钮消失 → 困惑 "我运行怎么不能重跑了?"
             - 修了配置后重跑还是老配置 → 困惑 "我明明改了 workflow 为什么没生效?"
预期系统行为:
             - Re-run 按钮在不可用时应有合理反馈: 灰掉时显示 tooltip 说明原因 (如 "已达最大重试次数 3 次" 或 "运行超过 6 小时, 不支持重新运行")。
             - 重新运行使用原始配置这一行为应在界面上有提示 (如 "正在使用运行 #42 时的 workflow 配置")。

Oracle 来源: `gitcode-spec/running-pipelines/rerun-failed-jobs.md` §重新运行限制

验证要点:
  - [正向] 连续 re-run 3 次后, 验证 Re-run 按钮禁用且有 tooltip 说明。
  - [正向] 对超过 6 小时的运行, 验证 Re-run 按钮禁用/消失且有说明。
  - [非功能] 重新运行详情页应有提示说明使用的是原始配置。

可理解性判据:
  - 确定性: 按钮禁用 + tooltip 是否存在 (可截图判定)。
  - `eval: llm_assisted`: tooltip 文字是否清晰易懂。

优先级线索: P2 (体验改善; 有 workaround: 重新 push 触发)
破坏级别:   none
来源输入:   `gitcode-spec/running-pipelines/rerun-failed-jobs.md`

---

## F. 复用与组合体验

---

意图 ID:    INTENT-USE-022
维度标签:   [usability, compatibility]
标题:       `workflow_call` 嵌套超过 2 层时的错误信息可诊断性

风险点:     GitCode 限制 `workflow_call` 最多嵌套 2 层 (COMPAT-NOTES.md §5)。GitHub 无此硬限制。若用户设计了 3 层嵌套的可复用 workflow, 第 3 层调用失败时的报错能否明确指出是 "超过最大嵌套层级 2" 而不是泛化的 "workflow call failed"?
预期系统行为: 当 `workflow_call` 嵌套超过 2 层时, 错误信息应明确指出:
              (1) 嵌套层级限制为 2 层;
              (2) 哪个 workflow 调用超出了限制;
              (3) 建议合并层级或改为直接调用。
Oracle 来源: COMPAT-NOTES.md §5; `gitcode-spec/writing-pipelines/configure-triggers.md` §workflow_call

验证要点:
  - [正向] 构造 A → B → C 三层 workflow_call 链, 触发 A, 验证 C 调用失败时的报错信息质量。

可理解性判据:
  - 确定性: 报错是否发生; 消息是否含 '2' (最大层级) 和 'nest'/'level' (层级) 关键词 (可判定)。
  - `eval: llm_assisted`: 消息是否足以让用户意识到需要精简层级 (而非怀疑是 bug)。

优先级线索: P2 (影响少数深度嵌套场景)
破坏级别:   none
来源输入:   COMPAT-NOTES.md §5; `gitcode-spec/writing-pipelines/configure-triggers.md`

---

意图 ID:    INTENT-USE-023
维度标签:   [usability]
标题:       `concurrency` 排队时用户的等待信息可见性

风险点:     `workflow-file-location-structure.md` 声明 `exceed-action: QUEUE` 支持排队。若排队时用户看不到排队位置/预计等待时间, 只能反复刷新页面猜测「是不是卡住了」。
预期系统行为: 当 workflow 因 concurrency 限制进入排队时, 运行详情页或 Actions 列表应显示:
              (1) 排队状态 (queued);
              (2) 排队位置 (如 "3rd in queue");
              (3) 若有预计开始时间则更佳。
Oracle 来源: `gitcode-spec/writing-pipelines/workflow-file-location-structure.md` §concurrency; `testing-focus.md` §9

验证要点:
  - [正向] 配置 `concurrency: { enable: true, max: 1, exceed-action: QUEUE }`, 连续触发 3 个 push, 观察第 2/3 个 run 的排队信息展示。
  - [非功能] 排队信息应在 Actions 列表页可见 (无需点进详情)。

可理解性判据:
  - 确定性: queued 状态是否展示; 排队序号是否展示 (可判定)。
  - `eval: llm_assisted`: 排队信息是否足以让用户判断「该等还是该取消」。

优先级线索: P2 (体验改善; concurrency 相对小众)
破坏级别:   none
来源输入:   `gitcode-spec/writing-pipelines/workflow-file-location-structure.md`; `testing-focus.md` §9

---

## 覆盖度自检

| 维度子类 | 覆盖 intent | 说明 |
|---|---|---|
| 错误信息质量 — 必填字段缺失 | INTENT-USE-001 | `on:` / `jobs:` 缺失 |
| 错误信息质量 — 类型错误 | INTENT-USE-002 | `runs-on` string vs list |
| 错误信息质量 — 未知字段 | INTENT-USE-003 | GitHub-only 字段静默忽略/报错 |
| 错误信息质量 — types 取值 | INTENT-USE-004 | PR types 命名差异报错 |
| 错误信息质量 — 表达式差异 | INTENT-USE-005 | `failure()` vs `failed` |
| 错误信息质量 — 上下文差异 | INTENT-USE-006 | `github.*` vs `atomgit.*` |
| 文档一致性 — 残留措辞 | INTENT-USE-007 | `GITHUB_*` 措辞残留 |
| 文档一致性 — environment | INTENT-USE-008 | `environment` 字段文档 vs 行为 |
| 文档一致性 — runner 返回值 | INTENT-USE-009 | `runner.os`/`runner.arch` 大小写 |
| 调试体验 — workflow commands | INTENT-USE-010 | `::group::`/`::error::`/`::warning::` |
| 调试体验 — 状态机 | INTENT-USE-011 | queued/cancelled/skipped 可见性 |
| 调试体验 — 系统变量 | INTENT-USE-012 | `ATOMGIT_*` 注入完整性 |
| 调试体验 — post 阶段 | INTENT-USE-013 | post 阶段展示 |
| 迁移摩擦 — 端到端 | INTENT-USE-014 | 直接搬 GitHub workflow 全路径 |
| 迁移摩擦 — runs-on | INTENT-USE-015 | GitHub 风格标签报错 |
| 迁移摩擦 — permissions | INTENT-USE-016 | GitHub 权限命名报错 |
| 迁移摩擦 — builtin actions | INTENT-USE-017 | `actions/checkout@v4` 报错 |
| 迁移摩擦 — inputs 类型 | INTENT-USE-018 | `type: boolean` 报错 |
| 迁移摩擦 — 迁移指南 | INTENT-USE-019 | 官方迁移文档完整性 |
| 重新运行 — 结果保留 | INTENT-USE-020 | cached job 日志保留 |
| 重新运行 — 限制反馈 | INTENT-USE-021 | 3次/6小时/原始配置 提示 |
| 嵌套调用 — 层级限制 | INTENT-USE-022 | 2层嵌套超限报错 |
| 并发排队 — 等待信息 | INTENT-USE-023 | 排队位置可见性 |

## 风险覆盖核对

| 风险 ID | 覆盖 intent | 说明 |
|---|---|---|
| RISK-USE-01 (迁移报错不指明 GitCode 差异) | USE-001/004/005/006/014/015/016/017/018/019 | 10 条 intent 从不同角度覆盖迁移报错质量 |

## 与现有用例的差异说明

本批 intent 与 `cases.md` 631 条现有用例的区别:
- 现有用例问: "这个 YAML 写法能不能跑通?"
- 本批 intent 问: "跑不通的时候, 报错信息能不能让开发者自己修好?"

本批 intent 与 compat-diff agent 的区别:
- compat-diff 关注: GitCode vs GitHub 的**行为差异** (对不对)
- usability 关注: 这些差异导致的**体验后果** (体验好不好, 报错看不看得懂)
