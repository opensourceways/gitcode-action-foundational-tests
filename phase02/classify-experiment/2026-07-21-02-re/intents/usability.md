# 易用性 Intent · GitCode Action（DevEx / 迁移摩擦 / 文档一致性）

> 产出 Agent：usability（开发者体验 DevEx 评审）
> Run：2026-07-21-02
> 视角：**一个从 GitHub Actions 迁过来的普通开发者**——验证「不是 bug 但很劝退」的体验、可理解性、迁移摩擦、文档质量。
> 来源输入：
> - `inputs/business-context/README.md`（2026-07-21，三大测试维度：文档易用性 / 实操易用性 / 竞品兼容性）
> - `inputs/gitcode-spec/`（fetched 2026-07-20，含 `COMPAT-NOTES.md` 差异速记、`01-quick-start.md`）
> - `inputs/workflow-samples/`（2026-07-21，cann / op-plugin 真实迁移素材）
> - 本 run `intents/spec.md` §2.4（G-21~G-32 文档自相矛盾/GitHub 残留措辞 12 条）
>
> **纪律**：
> - 错误信息类 intent 给「应包含什么」的**具体可确定判据**（如「应含行号」），不写「报错要友好」。
> - 主观评判项显式标 `eval: llm_assisted`（见 rules §3），不滥用。
> - 不与 compat-diff 重复：**易用性=体验/可理解**，兼容性=行为对不对。关联的兼容性差异在字段中注明（供交叉溯源）。
> - 覆盖从 GitHub 迁移的主要摩擦路径（见文末「摩擦路径覆盖矩阵」）。

---

## A. 迁移改造点摩擦：搬运即断，报错是否点明「这是 GitCode 差异」

```
意图 ID:    INTENT-USE-001
维度标签:   [usability, compatibility]
标题:       直接把 .github/workflows/ 搬到仓库根，workflow 是否静默不被识别（迁移第一摩擦点）

风险点:     GitCode 仅识别 `.gitcode/workflows/` 下的 `.yml`/`.yaml`（C-STRUCT-01）。从 GitHub 迁移的开发者第一反应是把整个 `.github/workflows/` 目录连同文件推上来。若平台对「文件在错误目录」既不触发也无任何提示，用户会陷入「推了没反应、不知道哪错了」的死胡同——这是最高频、最劝退的迁移入口摩擦。
预期系统行为: 放在 `.github/workflows/` 的 workflow 不被触发是可接受的；但平台应通过某种可发现的渠道（仓库 Actions 页提示 / 文档迁移指引置顶）让用户能自查「目录需从 .github 改为 .gitcode」，而非零反馈。
Oracle 来源: GitCode规格（01-quick-start.md:22 明确「目录路径错误会导致流水线无法被识别和触发」）

验证要点:
  - [正向] 文件置于 `.gitcode/workflows/xxx.yml` 时正常触发。
  - [负向] 文件置于 `.github/workflows/xxx.yml` 时不触发——确认这是静默行为（无 Actions 记录、无错误条目）。
  - [非功能] 评估「用户能否自助定位到目录问题」：是否有任一可发现的提示指向「.gitcode/workflows」。eval: llm_assisted（可发现性/上手成本属主观体验）。

可理解性判据: 客观部分——`.github/workflows/` 下文件不产生任何运行记录（可确定判定）。主观部分——是否存在可发现的目录纠错引导，标 eval: llm_assisted。
关联的兼容性差异: COMPAT-NOTES §1（目录 `.gitcode/workflows/` vs `.github/workflows/`）；compat-diff 验证「是否识别/触发」，本条验证「用户能否理解为何没反应」。
优先级线索: 关联迁移摩擦（testing-focus §11）；risk-register 模板态，建议门禁据 §11 定级。
来源输入:   inputs/gitcode-spec/01-quick-start.md（fetched 2026-07-20）；business-context/README.md 维度3「文件直接迁移适配」
```

```
意图 ID:    INTENT-USE-002
维度标签:   [usability, compatibility]
标题:       直接搬运含 ${{ github.* }} 上下文的 workflow，报错是否点明「应改用 atomgit.*」

风险点:     GitCode 核心上下文是 `atomgit.*`，GitHub 是 `github.*`（COMPAT-NOTES §2）。迁移改造点清单里「全局替换 github.* → atomgit.*」是必改项。若用户漏改，`${{ github.sha }}` 这类引用——按 context.md 语义「引用不存在属性求值为空字符串」（C-EXPR-06）——很可能静默求值为空串，导致脚本拿到空值继续跑，产生难以定位的下游错误，而非在表达式层就报「未知上下文 github」。
预期系统行为: 引用未知上下文对象 `github` 时，理想应给出可操作诊断（指出 `github` 非法上下文、建议 `atomgit`）；至少不应让空串静默流入脚本而无任何日志痕迹。
Oracle 来源: GitCode规格（syntax-reference/context.md:23-49 列 atomgit 属性；context.md 求值不存在属性为空串）

验证要点:
  - [正向] `${{ atomgit.sha }}` 正常展开为提交 SHA。
  - [负向] `${{ github.sha }}` 不应无声展开为空串却不留任何可诊断线索。
  - [非功能] 若确为静默空串，日志中是否有 warning 指向未知上下文。eval: llm_assisted（诊断线索充分性主观）。

可理解性判据:
  - 可确定：对比 `${{ github.sha }}` 与 `${{ atomgit.sha }}` 的展开值——前者为空/后者非空即坐实静默降级。
  - 主观：错误/警告信息是否点明「github 上下文不存在，GitCode 用 atomgit」→ eval: llm_assisted。
关联的兼容性差异: COMPAT-NOTES §2（上下文对象 atomgit.* vs github.*）。compat-diff 验证求值行为，本条验证「用户能否从提示中知道要改成 atomgit」。
优先级线索: 迁移摩擦高频（testing-focus §11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/context.md；COMPAT-NOTES.md §2
```

```
意图 ID:    INTENT-USE-003
维度标签:   [usability, compatibility]
标题:       GitHub 式状态函数 success()/failure()（带括号）的报错是否指明「GitCode 状态函数不带括号」

风险点:     GitCode 状态函数无括号：`if: ${{ success }}`/`failed`/`cancelled`/`always`；GitHub 是 `success()`/`failure()`（COMPAT-NOTES §3）。迁移者极易照抄 `if: ${{ success() }}` 或 `${{ failure() }}`。危险在于：`failure` 在 GitCode 根本不是函数名（GitCode 用 `failed`），若表达式引擎把 `failure()` 当未知标识符静默求值为假/空，会导致「本应在失败时跑的清理步骤永远不执行」——静默跳过比报错更难发现。
预期系统行为: 带括号写法或 `failure()` 应产生确定且可诊断的结果：要么报语法错误并提示「状态函数应写为 success/failed（无括号）」，要么明确不识别；不应静默恒假导致条件步骤被跳过而无提示。
Oracle 来源: GitCode规格（syntax-reference/expressions.md:36-54；COMPAT-NOTES §3）

验证要点:
  - [正向] `if: ${{ failed }}` 在前置失败时为真、成功时为假。
  - [负向] `if: ${{ success() }}` / `${{ failure() }}` 不应被静默当作恒真或恒假使条件步骤错误执行/跳过而无日志说明。
  - [非功能] 报错信息应包含「状态函数」「无括号」或等价指引。

可理解性判据: 错误信息应包含以下之一（可确定判定）：①出错的表达式原文；②「状态函数不带括号」或「未知函数 failure」的明示；③正确写法示例 `success`/`failed`。若三者皆无仅泛化「表达式错误」，判不合格。
关联的兼容性差异: COMPAT-NOTES §3（状态函数无括号 + failed vs failure()）；spec.md INTENT-COMP-008。compat-diff 验证求值语义，本条验证报错可理解性。
优先级线索: 迁移摩擦（testing-focus §1/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/expressions.md；COMPAT-NOTES.md §3
```

```
意图 ID:    INTENT-USE-004
维度标签:   [usability, compatibility]
标题:       跨 job 输出引用 needs.<job>.outputs（GitHub 式）在 GitCode 是否可用/报错是否指向 jobs.<job>.outputs

风险点:     真实样本 op-plugin PR-pipeline 用 `if: ${{ jobs.Only_doc_commit.outputs.build_skip != 'yes' }}` 引用跨 job 输出——GitCode 用 `jobs.<id>.outputs`，而 GitHub 用 `needs.<id>.outputs`（C-EXEC-06/C-EXPR-07）。迁移者照 GitHub 写 `needs.Only_doc_commit.outputs.build_skip`，若 GitCode 不识别 `needs` 上下文或求值为空，跨 job 依赖判据会静默失效——「本该跳过的 build 全跑了」或「本该跑的被跳过」，且无报错。
预期系统行为: `needs.*` 若非 GitCode 合法上下文，应产生可诊断结果（报错并提示 GitCode 用 `jobs.<id>.outputs` 访问上游输出），不应静默求空导致 if 判据反转。
Oracle 来源: GitCode规格（context.md:5-21 上下文清单；configure-jobs.md:139-150 outputs 经 jobs.<job>.outputs 访问）

验证要点:
  - [正向] `${{ jobs.<upstream>.outputs.<key> }}` 能取到上游 job 输出。
  - [负向] `${{ needs.<upstream>.outputs.<key> }}` 不应静默求值为空使下游 if 判据错误放行/拦截而无提示。
  - [非功能] 若 `needs` 不被支持，报错应指向正确写法。eval: llm_assisted（「是否足以引导用户改写」需主观判断）。

可理解性判据:
  - 可确定：对照 `jobs.` 与 `needs.` 两种写法下 if 判据的实际走向，坐实 needs 是否静默失效。
  - 主观：报错是否引导到 `jobs.<id>.outputs` → eval: llm_assisted。
关联的兼容性差异: 上下文对象差异（GitCode `jobs.` vs GitHub `needs.`）——compat-diff 可派生一致性用例。本条聚焦「静默失效的可发现性」。
优先级线索: 迁移摩擦 + 真实样本证据（testing-focus §3/§11）；risk-register 模板态。
来源输入:   inputs/workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:190；inputs/gitcode-spec/writing-pipelines/configure-jobs.md
```

```
意图 ID:    INTENT-USE-005
维度标签:   [usability, compatibility]
标题:       permissions 权限域用 GitHub 命名（contents/pull-requests）时的报错质量

风险点:     GitCode 权限域是 `project`/`pr`/`issue`/`note`/`repository`/`hook`；GitHub 是 `contents`/`pull-requests`/`issues`/`actions`（COMPAT-NOTES §6）。命名完全不同且迁移必改。用户照抄 `permissions: { contents: write, pull-requests: write }`，若平台静默忽略未知权限键，会导致「以为授了写权限、实际是仓库默认权限」的安全性+功能性双重隐患，且用户毫不知情。
预期系统行为: 未知权限域键（contents/pull-requests…）应被显式报错或至少 warning 列出「无法识别的权限域」，并指向 GitCode 权限域取值，而非静默丢弃。
Oracle 来源: GitCode规格（token-permissions.md:24-47 权限域；COMPAT-NOTES §6）

验证要点:
  - [正向] `permissions: { pr: write }` 被正确解析生效。
  - [负向] `permissions: { contents: write }` 不应被静默忽略（导致实际权限与声明不符且无提示）。
  - [非功能] 报错/警告应包含被拒绝的键名。

可理解性判据: 提示信息应包含以下（可确定判定）：①无法识别的权限键名原文（如 `contents`）；②GitCode 合法权限域列表或其中至少一个正确替代（如 `repository`/`pr`）。仅静默忽略无任何输出=不合格。
关联的兼容性差异: COMPAT-NOTES §6（permissions 权限域命名）。本条验证「未知键的反馈」，行为等价性归 compat-diff。
优先级线索: 迁移摩擦 + 安全相关（testing-focus §5/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/security-permissions/token-permissions.md；COMPAT-NOTES.md §6
```

```
意图 ID:    INTENT-USE-006
维度标签:   [usability, compatibility]
标题:       runs-on 用 GitHub 单标签 ubuntu-latest 迁移时的行为与可理解性

风险点:     GitCode 用三段式 `{os-version},{arch},{flavor}` 或 `default`（COMPAT-NOTES §7）；但 quick-start 示例又写 `runs-on: ubuntu-latest`（单标签，01-quick-start.md:34），文档内部就不一致。迁移者从 GitHub 带来大量 `runs-on: ubuntu-latest`。若单标签匹配规则是「所有标签须为 Runner 标签集合子集」（C-RUN-05），单个 `ubuntu-latest` 能否匹配到默认 Runner、还是因缺 arch/flavor 段而排不到 Runner 无限排队——直接决定「开箱能不能跑」。
预期系统行为: 要么 `ubuntu-latest` 被接受并映射到合理默认（体验友好），要么明确报「标签不完整/无匹配 Runner」并提示三段式写法；不应无限排队无反馈。
Oracle 来源: GitCode规格（selecting-runner-labels.md:19-35；01-quick-start.md:34 与三段式声明冲突）

验证要点:
  - [正向] `runs-on: default` 与三段式 `[ubuntu-latest, x64, small]` 能正常分配 Runner。
  - [负向] 单标签 `runs-on: ubuntu-latest` 若无法匹配，不应静默无限排队而无任何「无匹配 Runner」提示。
  - [非功能] 排不到 Runner 时应在合理时限内给出可理解报错（与 INTENT-USE-020 呼应）。

可理解性判据: 若单标签不被接受，报错应包含以下之一（可确定判定）：①「无可用 Runner 匹配标签 ubuntu-latest」；②缺失的标签段提示（arch/flavor）；③三段式正确写法示例。
关联的兼容性差异: COMPAT-NOTES §7（runs-on 三段式 vs 单标签）；spec.md G-27（数组式 vs 花括号式并存）。
优先级线索: 迁移摩擦「开箱能否跑」（testing-focus §4/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/runner-management/selecting-runner-labels.md；01-quick-start.md；COMPAT-NOTES.md §7
```

---

## B. 报错质量：语法/静态校验的可诊断性（错在哪、为什么、怎么改）

```
意图 ID:    INTENT-USE-007
维度标签:   [usability]
标题:       非法 YAML（缩进/语法错误）的报错是否精确到行号

风险点:     spec.md G-35 明确「非法 YAML/未知字段处理（报错 vs 静默忽略）文档未涉及」，且 workflow-job-step-action.md:22-40 示例 stages 缩进本身疑似错误（G-26）。workflow 文件是纯文本手写，缩进错误是最高频的低级失误。若报错只给「解析失败」而不给行号/列，用户在几十行的 YAML 里逐行猜，上手成本剧增。
预期系统行为: YAML 解析失败应指明出错位置（行号，最好含列/上下文片段）与错误类型（如「映射缩进不一致」）。
Oracle 来源: GitHub行为（GitHub Actions 对 YAML 错误给出行号定位，作为「大部分兼容」默认 oracle）；GitCode 规格未声明（G-35）

验证要点:
  - [正向] 合法 YAML 正常解析运行。
  - [负向] 缩进错误的 YAML 不应仅返回泛化「解析失败/内部错误」而无定位。
  - [非功能] 报错应包含行号。

可理解性判据: 错误信息**应包含出错行号**（可确定判定：断言报错文本中存在指向缺陷行的行号）。加分项（可确定）：错误类别描述、出错片段回显。仅「YAML 解析失败」无行号=不合格。
关联的兼容性差异: 无（纯报错质量）；与 compat-diff 的「未知字段处理」互补但不重复——本条聚焦定位精度。
优先级线索: 报错质量（testing-focus §1）；risk-register 模板态。
来源输入:   本 run spec.md G-35；inputs/gitcode-spec/core-concepts/workflow-job-step-action.md
```

```
意图 ID:    INTENT-USE-008
维度标签:   [usability, compatibility]
标题:       未知/不支持顶层字段（如 GitHub 的 defaults 之外拼写或 GitHub 专有字段）的处理：报错还是静默忽略

风险点:     GitCode 合法顶层字段集固定为 name/on/env/defaults/concurrency/permissions/stages/jobs/post（C-STRUCT-02）。迁移者可能带入 GitHub 有而 GitCode 语义不同/不存在的顶层键，或手滑拼错（`job:` vs `jobs:`）。静默忽略未知字段会让「以为配置生效、实际没生效」——比如拼错 `jobs` 为 `job`，若静默忽略则 workflow 无 job 可跑却不报错。
预期系统行为: 未知顶层字段应至少 warning 提示「无法识别的字段 X」；关键必填字段（jobs/on）缺失或拼错应报错而非静默产出空运行。
Oracle 来源: GitCode规格（C-STRUCT-02 顶层字段集）；GitHub行为（未知键给 warning）

验证要点:
  - [正向] 合法顶层字段集正常解析。
  - [负向] `job:`（拼错的 jobs）不应被静默忽略产生「无任何 job 执行且无报错」的空运行。
  - [非功能] 未知字段提示应包含字段名。

可理解性判据: 对拼错必填字段的情形，报错/警告**应包含被忽略或缺失的字段名**（可确定判定）。若产生空运行且无任何提示=不合格。
关联的兼容性差异: testing-focus §1「未知字段处理是兼容性差异高发区」；compat-diff 验证「静默忽略 vs 报错」的行为对标，本条验证「用户能否知道字段没生效」。
优先级线索: 报错质量 + 迁移摩擦（testing-focus §1/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md:54-66（C-STRUCT-02）
```

```
意图 ID:    INTENT-USE-009
维度标签:   [usability, compatibility]
标题:       事件名 pr_comment / pull_request_comment 混用时的报错可理解性（真实样本证据）

风险点:     真实样本自相矛盾：op-plugin 用 `on: pull_request_comment`（与文档 C-TRIG-05 一致），而 cann/sub_pipline_support.yaml 用 `on: pr_comment` + `keyword:`（文档里根本没有 `pr_comment` 事件、过滤键是 `comments` 不是 `keyword`）。这说明真实迁移/编写中事件名与过滤键极易写错。若写了不存在的事件名 `pr_comment` 平台静默不触发，用户会以为「评论触发没生效」而无从排查。
预期系统行为: 未知事件名（`pr_comment`）或未知过滤键（`keyword`）应在校验期报错，指明合法事件名/过滤键；不应静默产出「永不触发」。
Oracle 来源: GitCode规格（syntax-reference/trigger-events.md:127-160 定义 pull_request_comment + comments 过滤）

验证要点:
  - [正向] `on: pull_request_comment` + `comments: [正则]` 能被评论正确触发。
  - [负向] `on: pr_comment` + `keyword:` 不应静默注册为「永不触发」而无任何校验提示。
  - [非功能] 报错应包含未知事件名/键名。

可理解性判据: 报错应包含以下之一（可确定判定）：①未知事件名 `pr_comment` 原文；②合法事件名 `pull_request_comment`；③未知过滤键 `keyword` 及正确键 `comments`。
关联的兼容性差异: COMPAT-NOTES §5（pull_request_comment 为 GitCode 特有事件）。本条聚焦「写错时能否被诊断」，非行为对标。
优先级线索: 报错质量 + 真实样本证据（testing-focus §1/§2/§11）；risk-register 模板态。
来源输入:   inputs/workflow-samples/cann/sub_pipline_support.yaml；op-plugin/PR-pipeline_op-plugin.yml:12；trigger-events.md:127-160
```

```
意图 ID:    INTENT-USE-010
维度标签:   [usability, compatibility]
标题:       inputs 声明 GitHub 式 type: boolean/choice/number 时的报错是否指引「仅支持 string」

风险点:     GitCode 的 workflow_dispatch/workflow_call inputs 仅支持 string（COMPAT-NOTES §9 / C-VAR-07）。GitHub 支持 boolean/choice/number/environment。迁移者带来 `type: boolean` 的 inputs 极常见。若静默降级为字符串，`type:boolean` 的 'false' 在 `if` 中按非空字符串判真——产生与预期完全相反的分支走向，且无任何提示（这是安全+功能双敏感的静默陷阱）。
预期系统行为: 非 string 的 inputs type 应被明确处理——报错并提示「inputs 仅支持 string，请用 string + 表达式转换」，而非静默当字符串用。
Oracle 来源: GitCode规格（syntax-reference/variables.md:56-62；manually-trigger-pipeline.md:54）

验证要点:
  - [正向] `type: string` 的 inputs 正常，默认值/引用生效。
  - [负向] `type: boolean` 的 'false' 不应因静默转字符串在 if 中被判真（分支反转）而无提示。
  - [非功能] 报错应指明「仅支持 string」。

可理解性判据: 若拒绝非 string type，报错**应包含**「string」字样及被拒的 type 名（可确定）；若接受则降级规则须文档化。判定证据=非法 type 是否产出可见报错文本。
关联的兼容性差异: COMPAT-NOTES §9；spec.md INTENT-COMP-005。compat-diff 验证「报错 vs 静默降级」的行为，本条验证「提示是否引导到 string」。
优先级线索: 迁移摩擦 + 静默语义陷阱（testing-focus §1/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/variables.md；COMPAT-NOTES.md §9
```

```
意图 ID:    INTENT-USE-011
维度标签:   [usability, compatibility]
标题:       引用带 owner/版本的 GitHub action（actions/checkout@v4）时的报错可理解性

风险点:     GitCode 内置 action 用无 owner 短名 `checkout`/`setup-node`（COMPAT-NOTES §10）；GitHub 用 `actions/checkout@v4`。迁移者的 workflow 里全是 `uses: actions/checkout@v4`。若 GitCode 尝试按 `owner/repo@ref` 去解析 `actions/checkout@v4` 而找不到、报「action 拉取失败/仓库不存在」的泛化网络错，用户不会联想到「应改用短名 checkout」。
预期系统行为: 对无法解析的 `actions/checkout@v4` 这类常见 GitHub 内置 action 引用，报错最好能提示 GitCode 对应短名；至少应明确「解析失败的是哪个 uses 引用」而非笼统失败。
Oracle 来源: GitCode规格（using-actions.md:44-100 内置短名与 owner/repo@ref 引用）

验证要点:
  - [正向] `uses: checkout` 正常运行 checkout。
  - [负向] `uses: actions/checkout@v4` 若不支持，不应给出与真实原因无关的泛化报错（如纯网络超时）。
  - [非功能] 报错应包含出错的 uses 引用原文。eval: llm_assisted（是否提示到短名替代属主观充分性）。

可理解性判据:
  - 可确定：报错文本应包含失败的 `uses` 引用字符串（如 `actions/checkout@v4`）。
  - 主观：是否提示 GitCode 对应短名 `checkout` → eval: llm_assisted。
关联的兼容性差异: COMPAT-NOTES §10（内置 action 短名 vs owner/版本）。本条聚焦报错可理解性，等价实现行为归 compat-diff。
优先级线索: 迁移摩擦（testing-focus §7/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/writing-pipelines/using-actions.md；COMPAT-NOTES.md §10
```

```
意图 ID:    INTENT-USE-012
维度标签:   [usability]
标题:       废弃命令 ::set-output/::set-env/::add-path 使用时是否给出可操作的迁移提示

风险点:     GitCode 已废弃 `::set-output`/`::set-env`/`::add-path`，改用 `>> $ATOMGIT_OUTPUT` 文件协议（C-ACT-03 / COMPAT-NOTES §11）。但 spec.md G-24 指出：插件开发指南自身示例仍在用 `::set-output var=`（且语法 `var=` 与正文 `name=` 不一致）——连官方文档都混用。迁移者从旧 GitHub workflow 带来 `echo "::set-output name=x::y"` 极普遍。若废弃命令被静默无视（output 未设置）且无 deprecation 提示，下游取不到 output 却不知为何。
预期系统行为: 使用废弃命令时应输出 deprecation warning，指明命令已废弃及替代写法（`>> $ATOMGIT_OUTPUT`），而非静默丢弃。
Oracle 来源: GitCode规格（workflow-commands.md:60-68 废弃声明）；GitHub行为（GitHub 对同类废弃命令给 warning）

验证要点:
  - [正向] `echo "k=v" >> "$ATOMGIT_OUTPUT"` 正确设置输出。
  - [负向] `echo "::set-output name=k::v"` 不应静默无效且无任何 deprecation 提示。
  - [非功能] warning 应包含替代写法关键字 `ATOMGIT_OUTPUT`。

可理解性判据: 使用废弃命令时，日志**应包含 deprecation 提示**且提示中含替代关键字 `ATOMGIT_OUTPUT`（可确定判定）。静默无输出=不合格。
关联的兼容性差异: 无（GitCode 与 GitHub 演进一致）；纯 DevEx。关联文档缺陷 G-24。
优先级线索: 报错/调试质量（testing-focus §1/§9）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/workflow-commands.md；本 run spec.md G-24
```

---

## C. 文档一致性/质量：文档承诺 vs 实际，及文档自相矛盾（G-21~G-32）

> 这些 intent 的可理解性判据多为「以实测确立唯一权威值，文档矛盾本身即缺陷」。文档措辞友好度类标 eval: llm_assisted；「文档两处取值是否冲突」可客观核对。

```
意图 ID:    INTENT-USE-013
维度标签:   [usability, security]
标题:       permissions:{} 实际权限与文档两处冲突声明的核对（能否 clone 代码）

风险点:     spec.md G-21：`permissions: {}` 一处称「全 none」，一处称「仅 repository:read」。用户用最小权限模式时，这直接决定 job 能否 checkout 代码。文档自相矛盾使用户无法从文档预判行为——是纯粹的文档质量缺陷，也影响最小权限实践的可用性。
预期系统行为: `permissions: {}` 有唯一确定实际权限集，文档应统一到该值；用户能据文档预判 checkout 是否可用。
Oracle 来源: 差异声明（两处 GitCode 文档冲突，实测确立权威值回写 Parity Matrix）

验证要点:
  - [正向] 设 `permissions: {}` 后可确定 ATOMGIT_TOKEN 实际权限集（能否 clone）。
  - [负向] 不应出现「文档 A 说 none、实际能 clone」这类与两处声明都无法对齐且无记录的行为。
  - [非功能] 实测结果应能消解文档矛盾。

可理解性判据: 文档缺陷可确定判定——核对两处文档确认表述冲突存在（客观）。行为判据：实测 `permissions:{}` 下 checkout 成功/失败为唯一结果，与至少一处文档一致。产出 usability 文档勘误项。
关联的兼容性差异: 无对标 GitHub；此为 GitCode 内部文档一致性。与 spec.md INTENT-COMP-006 同源，本条从「文档可信度/用户能否预判」角度立。
优先级线索: 文档质量 + 安全实践可用性（testing-focus §5/§11）；risk-register 模板态。
来源输入:   本 run spec.md G-21；workflow-file-location-structure.md:216-223 vs token-permissions.md:103
```

```
意图 ID:    INTENT-USE-014
维度标签:   [usability, reliability]
标题:       重跑后 ATOMGIT_RUN_ID 是否变化——两文档冲突导致用户无法用作幂等键

风险点:     spec.md G-22：rerun 页称重跑后 RUN_ID 更新，运行时变量页称 RUN_ID 不变仅 RUN_ATTEMPT 递增。用户常以 RUN_ID 作追踪/幂等键（如产物命名、去重）。文档矛盾使用户不敢依赖 RUN_ID 语义——文档质量缺陷直接损害可用性。
预期系统行为: RUN_ID 跨重跑有唯一确定语义（稳定或变化二选一），文档统一，RUN_ATTEMPT 每次重跑递增。
Oracle 来源: 差异声明（两处 GitCode 文档冲突，实测定权威）

验证要点:
  - [正向] 触发一次运行并重跑，记录 RUN_ID/RUN_NUMBER/RUN_ATTEMPT 前后值。
  - [负向] RUN_ID 语义不应含糊到用户无法据其做幂等键。
  - [非功能] 实测消解矛盾，产出勘误。

可理解性判据: 客观——核对两文档确认冲突存在；实测得 RUN_ID 跨重跑的唯一行为。文档应据实测统一表述。判定为文档一致性缺陷（可确定：两处表述矛盾即成立）。
关联的兼容性差异: 无；GitCode 内部一致性。与 spec.md INTENT-COMP-007 同源，本条聚焦「用户可预期性」。
优先级线索: 文档质量 + 可观测性（testing-focus §9）；risk-register 模板态。
来源输入:   本 run spec.md G-22；rerun-failed-jobs.md:25 vs runtime-environment-variables.md:36
```

```
意图 ID:    INTENT-USE-015
维度标签:   [usability, compatibility]
标题:       系统变量命名 RUNNER_OS vs ATOMGIT_RUNNER_OS 两套并存导致用户不知该用哪个

风险点:     spec.md G-23：两文档给出 `RUNNER_OS/ARCH` 与 `ATOMGIT_RUNNER_OS/ARCH` 两套前缀命名。用户在脚本里引用系统变量时不知哪个真实存在——若只有一个生效、另一个为空，脚本静默拿到空值。文档不一致直接制造迁移与调试摩擦。
预期系统行为: 系统变量有唯一确定命名（或明确两者皆注入为别名），文档统一说明；用户引用能拿到值。
Oracle 来源: GitCode规格（runtime-environment-variables.md:47-52 vs using-variables-secrets.md:136-138 冲突）

验证要点:
  - [正向] 文档主推的系统变量名能在脚本中取到 Runner OS/ARCH 值。
  - [负向] 文档提及但实际不注入的变量名不应静默为空却无说明。
  - [非功能] 确认两套命名哪套真实存在、是否互为别名。

可理解性判据: 客观——实测 `echo $RUNNER_OS` 与 `echo $ATOMGIT_RUNNER_OS` 各自是否有值（可确定判定）；文档应据结果统一。文档矛盾成立即记 usability 缺陷。
关联的兼容性差异: G-23 关联 compat（GitHub 用 RUNNER_OS）。本条聚焦「文档双命名让用户困惑」，具体值对标归 compat-diff。
优先级线索: 文档质量 + 迁移摩擦（testing-focus §11）；risk-register 模板态。
来源输入:   本 run spec.md G-23；runtime-environment-variables.md:47-50 vs using-variables-secrets.md:136-138
```

```
意图 ID:    INTENT-USE-016
维度标签:   [usability]
标题:       文档夹带 GitHub 残留措辞（octocat/actions/checkout/GITHUB_*）误导迁移者

风险点:     spec.md G-31：runtime-environment-variables.md 夹带 `octocat/Hello-World`、`actions/checkout` 等 GitHub 残留示例值；COMPAT-NOTES §2 亦注「部分描述文案仍夹带 GITHUB_ACTION_PATH 等 GitHub 残留措辞」。迁移者看到官方文档里出现 GitHub 命名，会误以为 GitCode 也支持 `github.*`/`GITHUB_*`/`actions/checkout`，加深「照 GitHub 写就行」的错误预期——文档残留直接制造迁移陷阱。
预期系统行为: 官方文档示例值应统一为 GitCode 命名（atomgit/ATOMGIT_*/短名 action），不出现 GitHub 专有标识（octocat、actions/*、GITHUB_*）作为 GitCode 行为的示例。
Oracle 来源: GitCode规格（文档应自洽，以 COMPAT-NOTES/spec.md 认定的 GitCode 命名为准）

验证要点:
  - [正向] 文档示例使用 atomgit.*/ATOMGIT_* 命名。
  - [负向] 文档不应出现 GITHUB_*/octocat/actions-owner 前缀作为 GitCode 示例值。
  - [非功能] 残留措辞是否会让迁移者产生错误预期。eval: llm_assisted（误导程度主观）。

可理解性判据:
  - 可确定：在指定文档页 grep GitHub 专有标识（`GITHUB_`、`octocat`、`actions/`）命中即坐实残留（可确定判定，附命中行号）。
  - 主观：残留是否显著误导 → eval: llm_assisted。
关联的兼容性差异: COMPAT-NOTES §2 残留措辞注记；G-31。纯文档质量，不涉行为对标。
优先级线索: 文档质量（testing-focus §11）；risk-register 模板态。
来源输入:   本 run spec.md G-31；COMPAT-NOTES.md §2；runtime-environment-variables.md
```

```
意图 ID:    INTENT-USE-017
维度标签:   [usability, compatibility]
标题:       stages 两种写法（列表 - name: vs 映射 stage1:）并存且示例缩进疑误，用户无所适从

风险点:     spec.md G-26：stages 文档多处混用「列表项 `- name:`」与「映射 `stage1:`」两种写法，且 workflow-job-step-action.md:22-40 示例 stages 缩进疑似错误。真实样本 op-plugin 用映射式 `stage_1:`。stages 是 GitCode 特有编排机制（GitHub 无），迁移者本就陌生，文档还给两套写法+疑似错误示例，抄哪个都可能踩坑。
预期系统行为: stages 应有唯一推荐写法（或明确声明两种等价），示例缩进正确可直接复制运行。
Oracle 来源: GitCode规格（configure-dependencies-order.md 两处写法；应实测确认等价性）

验证要点:
  - [正向] 文档某一种 stages 写法可原样复制并成功运行。
  - [负向] 疑似缩进错误的示例不应被用户原样复制导致解析失败。
  - [非功能] 两种写法是否真等价、示例是否可直接复刻。eval: llm_assisted（示例「可直接复刻」含主观体验）。

可理解性判据:
  - 可确定：将文档 stages 示例原样提取运行，能否解析成功（成功/失败为客观结果）；核对两种写法是否都被接受。
  - 主观：写法二义性对新手的困扰 → eval: llm_assisted。
关联的兼容性差异: stages 为 GitCode 特有（COMPAT-NOTES §4）。本条聚焦「文档写法一致性/可复刻」，非与 GitHub 对标。
优先级线索: 文档质量 + 特有能力上手（testing-focus §3/§11）；risk-register 模板态。
来源输入:   本 run spec.md G-26；configure-dependencies-order.md:49-73,156-192
```

```
意图 ID:    INTENT-USE-018
维度标签:   [usability]
标题:       示例文档「可直接复刻」验证：quick-start 最小示例与内置 action 示例开箱可跑

风险点:     business-context 维度1 测试重点明列「步骤是否可直接复刻、示例可复用性」。quick-start 最小示例用 `runs-on: ubuntu-latest`（单标签，与三段式声明冲突，见 INTENT-USE-006），若照抄跑不起来，新手第一步就受挫。示例可复刻性是文档友好度的硬指标。
预期系统行为: 官方 quick-start 及各语言 CI 示例（nodejs/java-maven/go/python）应能原样复制到 `.gitcode/workflows/` 后成功运行，无需额外未文档化的改动。
Oracle 来源: GitCode规格（examples/ 各示例与 01-quick-start.md 承诺可开箱运行）

验证要点:
  - [正向] quick-start 最小 YAML 原样提交后成功产出「Hello GitCode Action」。
  - [负向] 示例不应需要文档未提及的隐性改动（如把 ubuntu-latest 改三段式）才能跑通。
  - [非功能] 从复制到成功的步骤数/摩擦点。eval: llm_assisted（上手顺畅度主观）。

可理解性判据:
  - 可确定：示例原样运行的成功/失败是客观结果；若失败，记录「文档未提及的必需改动」清单（可枚举即客观）。
  - 主观：整体上手顺畅度 → eval: llm_assisted。
关联的兼容性差异: 与 INTENT-USE-006 呼应（runs-on 单标签摩擦）。
优先级线索: 文档易用性核心指标（business-context 维度1；testing-focus §11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/01-quick-start.md；examples/*；business-context/README.md 维度1
```

```
意图 ID:    INTENT-USE-019
维度标签:   [usability, completeness]
标题:       日志/示例引用 atomgit.actor 但 context 属性表未列，用户按文档引用取到空值

风险点:     spec.md G-28：`atomgit.actor`/`atomgit.actor_id` 被 view-job-logs/example 页引用，但 context.md 属性表未列该属性。若用户照日志页示例写 `${{ atomgit.actor }}`，而该属性实际不存在（求值为空串，C-EXPR-06），会静默拿到空值。文档内部对「有哪些上下文属性」不一致，使用户无法判断 actor 是否可用。
预期系统行为: `atomgit.actor` 要么真实可用且在 context 属性表补齐，要么示例移除；用户据文档能确定该属性是否存在。
Oracle 来源: GitCode规格（context.md:23-49 属性表 vs view-job-logs.md:42 引用，冲突）

验证要点:
  - [正向] 若 actor 可用，`${{ atomgit.actor }}` 展开为触发者标识且属性表补齐。
  - [负向] 若不可用，不应因示例引导用户使用而静默返回空串无提示。
  - [非功能] 文档「示例引用的属性」与「属性表」应一致。

可理解性判据: 客观——实测 `${{ atomgit.actor }}` 是否有值（可确定）；核对 context.md 属性表是否缺列（可确定）。二者不一致即记文档缺陷。
关联的兼容性差异: G-28 关联 completeness（GitHub 有 github.actor）；本条聚焦文档自洽与用户可预期性。
优先级线索: 文档质量（testing-focus §9/§11）；risk-register 模板态。
来源输入:   本 run spec.md G-28；context.md:23-49 vs view-job-logs.md:42
```

---

## D. 调试体验 / 可观测性：日志、注解、状态回写、失败可诊断性

```
意图 ID:    INTENT-USE-020
维度标签:   [usability, reliability]
标题:       请求未开通规格（large+）或无匹配 Runner 时，排队是否有可理解反馈而非静默挂起

风险点:     spec.md INTENT-COMP-001 指出托管默认仅 slim/small/medium，large+ 需申请（C-RUN-03）。迁移者的 GitHub workflow 可能用大规格，或 runs-on 标签写错（见 INTENT-USE-006）。若排不到 Runner 时运行静默停在「排队中」无任何原因说明，用户会长时间等待并误以为平台卡死——这是可观测性缺失导致的劝退。
预期系统行为: 无法匹配 Runner（规格未开通/标签不存在）时，应在合理时限内于运行详情页给出可理解状态（如「无可用 Runner 匹配标签 X / 规格 large 需申请」），而非无限「排队中」无说明。
Oracle 来源: GitCode规格（using-hosted-runners.md:34「需申请」；selecting-runner-labels.md 匹配规则）

验证要点:
  - [正向] slim/small/medium 正常调度。
  - [负向] 请求未开通 large 或不存在的标签组合，不应静默无限排队且无任何原因提示。
  - [非功能] 无匹配 Runner 的反馈应在合理时限内出现，且状态文案包含原因。

可理解性判据: 排队超出合理阈值（如实测阈值 N 分钟，由门禁定）后，运行详情**应展示包含原因的状态文案**（含「Runner」「标签」或「规格/申请」关键字之一，可确定判定）。纯「排队中」无原因=不合格。
关联的兼容性差异: COMPAT-NOTES §7（规格档位）；spec.md INTENT-COMP-001。本条聚焦「等待期的可观测性」。
优先级线索: 可观测性 + 迁移摩擦（testing-focus §4/§9/§12）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/runner-management/using-hosted-runners.md；本 run spec.md INTENT-COMP-001
```

```
意图 ID:    INTENT-USE-021
维度标签:   [usability, security]
标题:       secret 脱敏在日志中的可观测性——用户误 echo secret 时能否看出被遮蔽

风险点:     C-SEC-03 文档自承 `echo "${{ secrets.X }}"` 可能绕过脱敏。从 DevEx 角度：用户调试时常 echo 变量排错，若一个值是 secret，日志里应显示 `***` 让用户意识到「这是敏感值、别打印」。若脱敏不一致（有时 `***`、有时明文），用户既无法调试又可能泄密而不自知。这里 usability 关注「用户能否从日志判断某值是否被当作 secret 保护」，与 security 的「是否真泄露」互补。
预期系统行为: secret 值在日志中一致显示为 `***`；用户能据此识别哪些值被保护。文档应明示「echo secret 仍可能泄露」的边界（已明示，属正确的诚实文档）。
Oracle 来源: GitCode规格（variables.md:48；using-variables-secrets.md:116-120）

验证要点:
  - [正向] 直接引用 secret 的日志输出显示 `***`。
  - [负向] 不应出现「用户以为被脱敏、实际明文」而日志无任何区分线索的情形。
  - [非功能] 脱敏呈现是否让用户对「值受保护」有明确认知。eval: llm_assisted（认知清晰度主观）。

可理解性判据:
  - 可确定：直接 `${{ secrets.X }}` 输出中是否出现 `***`（可确定判定）。
  - 主观：用户能否从日志建立「此值受保护」的正确心智 → eval: llm_assisted。
关联的兼容性差异: 无；与 security 维度（G-16 脱敏绕过的 negative 断言）互补——security 测「是否泄露」，本条测「用户可感知性」。不重复。
优先级线索: 可观测性 + 安全体验（testing-focus §5/§9）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/variables.md；using-variables-secrets.md；本 run spec.md G-16
```

```
意图 ID:    INTENT-USE-022
维度标签:   [usability]
标题:       job/step 失败时日志能否定位到「哪个 step、哪条命令、退出码」

风险点:     testing-focus §9 要求退出码语义、日志按 step 分组可读。真实样本（op-plugin）单个 job 有 checkout→setup-python→install→pre-commit 多 step 串行，任一失败时，用户需要快速定位是哪个 step、哪条 run 命令、退出码几。若失败日志笼统折叠或不标退出码，调试成本高。这是 CI 日常最高频的调试场景。
预期系统行为: 运行详情按 stage→job→step 结构展示（C-OBS-02），失败 step 可展开看到失败命令输出与非零退出码，能一眼定位失败点。
Oracle 来源: GitCode规格（view-run-results.md:29-68 结构；view-job-logs.md 日志能力）；GitHub行为（GitHub 失败 step 高亮+退出码）

验证要点:
  - [正向] 多 step job 中某 step `exit 1`，运行详情高亮/定位到该失败 step。
  - [负向] 失败原因不应被折叠到无法定位到具体 step 的程度。
  - [非功能] 日志应包含失败 step 名与退出码。

可理解性判据: 失败运行的日志/详情**应包含**：①失败 step 的标识（name 或 id）；②非零退出码数值。二者可确定判定。缺失退出码或无法定位 step=不合格。
关联的兼容性差异: 无；纯调试体验。
优先级线索: 可观测性（testing-focus §9）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/running-pipelines/view-run-results.md；view-job-logs.md；样本 op-plugin
```

```
意图 ID:    INTENT-USE-023
维度标签:   [usability]
标题:       workflow 命令注解 ::error::/::warning:: 能否在运行详情中可见并定位

风险点:     testing-focus §9 列 `::error::`/`::warning::`/`::group::` 等 workflow 命令与注解落到 PR/commit 的正确性。迁移者的 workflow 依赖这些注解在 UI 上高亮错误。若 GitCode 对这些命令静默当普通 echo 输出、不渲染为注解，用户失去结构化错误提示能力——体验倒退但无报错。
预期系统行为: `::error::msg` / `::warning::msg` 应被渲染为可识别的错误/警告注解（而非普通日志行），`::group::` 应折叠分组。
Oracle 来源: GitCode规格（workflow-commands.md workflow 命令集）；GitHub行为（注解渲染）

验证要点:
  - [正向] `echo "::error::something"` 在运行详情呈现为错误注解（区别于普通输出）。
  - [负向] 不应把 `::error::` 当普通文本原样打印而不渲染。
  - [非功能] 注解可见性/可定位性。eval: llm_assisted（「是否足够醒目可用」含主观）。

可理解性判据:
  - 可确定：`::error::` 输出是否与普通 echo 有可区分的呈现（渲染为注解 vs 原样文本），可确定判定。
  - 主观：注解醒目度/实用性 → eval: llm_assisted。
关联的兼容性差异: testing-focus §9 可观测性；内置 workflow 命令等价性可交 compat-diff，本条聚焦「用户能否看到结构化提示」。
优先级线索: 可观测性（testing-focus §9）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/syntax-reference/workflow-commands.md
```

```
意图 ID:    INTENT-USE-024
维度标签:   [usability]
标题:       PR 场景状态回写（Checks/commit status）到 PR 页的可见性与可理解性

风险点:     testing-focus §9 列状态回写（commit status/check run）与注解落到 PR 的正确性；C-OBS-01 列三入口（Actions/Commits/PR Checks）。真实样本均为 PR 触发流水线，开发者主要在 PR 页看「CI 过没过」。若运行状态不回写到 PR Checks、或回写的名称/状态与实际不符，reviewer 无法据 PR 判断是否可合入——迁移者从 GitHub 带来的「PR 门禁」心智直接落空。
预期系统行为: PR 触发的 workflow 运行状态应回写到 PR 页（成功/失败/运行中可见），状态项名称可关联到具体 workflow/job，点击可跳详情。
Oracle 来源: GitCode规格（view-run-results.md:9-27 三入口含 PR Checks）；GitHub行为（PR checks 回写）

验证要点:
  - [正向] PR 触发的运行在 PR 页显示对应状态项，状态与实际运行结果一致。
  - [负向] 运行失败时 PR 页状态不应仍显示成功/无状态（误导 reviewer）。
  - [非功能] 状态项能否关联并跳转到运行详情。eval: llm_assisted（关联清晰度主观）。

可理解性判据:
  - 可确定：PR 页状态项的成功/失败是否与实际运行结果一致（可确定判定）。
  - 主观：状态项命名与跳转的清晰度 → eval: llm_assisted。
关联的兼容性差异: 状态回写机制等价性可交 compat-diff；本条聚焦「PR 门禁体验是否成立」。
优先级线索: 可观测性 + PR 工作流迁移（testing-focus §9/§11）；risk-register 模板态。
来源输入:   inputs/gitcode-spec/running-pipelines/view-run-results.md；样本 op-plugin PR-pipeline
```

```
意图 ID:    INTENT-USE-025
维度标签:   [usability]
标题:       inputs 默认值在 shell 中以 ${var} 直接引用（真实样本写法）是否可用/失败可诊断

风险点:     真实样本 op-plugin 在 run 脚本里写 `--org_name ${org_name} --pr_id ${pr_id} --repo ${repo}`（第121行），直接用 shell 变量语法引用 inputs 名，而 inputs 定义在顶层 `inputs:` 块。GitCode 中 inputs 是否自动注入为同名 shell 环境变量并不明确（对比：action inputs 生成 `INPUT_<NAME>`，C-ACT-14）。若 `${org_name}` 在 shell 里是未定义变量（空），命令静默拿到空参数，反污染下游逻辑且无报错。这是「表达式上下文变量」与「shell 环境变量」混淆的高频真实摩擦。
预期系统行为: 要么 workflow 级 inputs 被注入为可在 run 中引用的环境变量（则 `${org_name}` 有值），要么明确不注入（用户需用 `${{ inputs.org_name }}` 表达式）；无论哪种，未定义变量导致的空参数不应完全无迹可循。
Oracle 来源: GitCode规格（C-VAR-01 变量体系；C-ACT-14 action inputs 注入 INPUT_*；workflow 级 inputs 注入方式文档未明——关联 G 类缺口）

验证要点:
  - [正向] 用文档支持的方式引用 inputs（如 `${{ inputs.x }}` 或注入的环境变量）能取到值。
  - [负向] `${org_name}` 若为未定义 shell 变量，不应静默以空值执行命令且无任何线索（如 `set -u` 缺失导致空展开）。
  - [非功能] 文档是否清晰说明 workflow 级 inputs 在 run 中的引用方式。eval: llm_assisted（文档清晰度主观）。

可理解性判据:
  - 可确定：对照 `${org_name}`（shell 语法）与 `${{ inputs.org_name }}`（表达式语法）两种引用下命令实际收到的参数值（空/非空），坐实哪种可用。
  - 主观：文档对两种语法边界的说明清晰度 → eval: llm_assisted。
关联的兼容性差异: 无直接 GitHub 对标；属 GitCode 上下文引用语义的可理解性。真实样本证据。
优先级线索: 迁移摩擦 + 静默空值陷阱（testing-focus §1/§11）；risk-register 模板态。
来源输入:   inputs/workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:16-36,121；inputs/gitcode-spec/writing-pipelines/using-variables-secrets.md
```

---

## 摩擦路径覆盖矩阵（自检）

> 覆盖「从 GitHub 迁移的主要摩擦路径」，对齐 business-context 三维度与 testing-focus §1/§9/§11。

| 迁移摩擦路径 | 覆盖 intent | 类型 |
|---|---|---|
| 文件目录 `.github/`→`.gitcode/` | USE-001 | 结构 |
| 上下文 `github.*`→`atomgit.*` | USE-002 | 命名 |
| 状态函数 `success()`→`success` | USE-003 | 表达式 |
| 跨 job 输出 `needs.`→`jobs.` | USE-004 | 表达式 |
| 权限域 `contents`→`pr/repository` | USE-005 | 权限 |
| `runs-on` 单标签→三段式 | USE-006, USE-018, USE-020 | Runner |
| YAML/未知字段报错质量 | USE-007, USE-008 | 静态校验 |
| 事件名/过滤键写错（pr_comment/keyword） | USE-009 | 触发器 |
| inputs 类型 `boolean`→`string` | USE-010 | 类型 |
| action 引用 `actions/checkout@v4`→短名 | USE-011 | 供应链 |
| 废弃命令 `::set-output` 提示 | USE-012 | 命令 |
| 文档自相矛盾（权限/RUN_ID/变量名/stages/actor） | USE-013,014,015,017,019 | 文档质量 |
| 文档 GitHub 残留措辞 | USE-016 | 文档质量 |
| 示例可复刻性 | USE-018 | 文档质量 |
| 调试可观测性（Runner 排队/脱敏/失败定位/注解/PR 回写） | USE-020,021,022,023,024 | 可观测性 |
| inputs shell 引用混淆（真实样本） | USE-025 | 变量语义 |

**llm_assisted 标注统计**：25 条中，含 `eval: llm_assisted` 分量的 = USE-001,002,004,011,016,017,018,020(部分),021,023,024,025 → **12 条**（约 48%），且均为「可确定判据 + 主观分量分离」式标注（客观部分仍给确定判据，仅体验/充分性/误导度等主观分量交 LLM 辅助），未滥用为整条主观。纯客观可判定（无 llm_assisted）= USE-003,005,006,007,008,009,010,012,013,014,015,019,022 → 13 条。

**溯源**：全部 intent 关联 testing-focus §1/§9/§11 与 business-context 三维度；文档质量类直接对应 spec.md G-21~G-32；真实样本类（USE-004,009,025）附样本行号证据。优先级线索因 risk-register 为模板态统一标注「模板态」，交门禁据 testing-focus 章节定级。

