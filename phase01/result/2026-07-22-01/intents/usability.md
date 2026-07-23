# Usability Intents（易用性维度）

> 产出时间：2026-07-22
> 维度 Agent：usability
> 输入退化标注：
> - `inputs/business-context/`：⚠️ 仅 README.md，无迁移规模/改造点/已知摩擦记录 —— 易用性 intent 将偏通用，缺真实场景骨架
> - `inputs/workflow-samples/`：⚠️ 仅 README.md，无真实样本 YAML 内容作迁移素材

---

## 1. 迁移摩擦扫描结果（按差异类别）

### 1.1 语法与命名差异（高频摩擦）

| 差异项 | GitHub 写法 | GitCode 写法 | 迁移摩擦点 | 对应 Intent |
|---|---|---|---|---|
| 工作流文件目录 | `.github/workflows/` | `.gitcode/workflows/` | 直接搬运后 workflow 不被识别；报错是否明示目录差异 | USE-MIGRATE-001 |
| 上下文对象 | `github.*` (`github.ref`, `github.sha`) | `atomgit.*` (`atomgit.ref`, `atomgit.sha`) | 表达式全线失效；报错是否指明「GitCode 使用 atomgit 上下文」 | USE-MIGRATE-002 |
| 系统环境变量 | `GITHUB_*` (`GITHUB_SHA`, `GITHUB_OUTPUT`) | `ATOMGIT_*` (`ATOMGIT_SHA`, `ATOMGIT_OUTPUT`) | Shell 脚本引用空值；是否给出变量映射指引 | USE-MIGRATE-003 |
| 状态函数 | `success()` / `failure()` / `always()` | `success` / `failed` / `always` | `if` 条件语法报错；是否指出「GitCode 状态函数不带括号」 | USE-MIGRATE-004 |
| 权限域命名 | `contents` / `pull-requests` / `issues` / `actions` | `repository` / `pr` / `issue` / `note` / `hook` | permissions 字段不识别；是否给出 GitCode 权限域对照 | USE-MIGRATE-005 |

### 1.2 执行环境与编排差异

| 差异项 | GitHub 写法 | GitCode 写法 | 迁移摩擦点 | 对应 Intent |
|---|---|---|---|---|
| Runner 标签 | `ubuntu-latest` / `self-hosted` + 自定义标签 | `{os,arch,flavor}` 三段式 或 `default` | `runs-on` 不匹配导致 job 无法调度；报错是否列出可用标签格式 | USE-MIGRATE-006 |
| Action 引用 | `actions/checkout@v4` / `owner/repo@ref` | `checkout` / `owner/repo/path@ref` | `uses` 写法差异；是否给出引用格式对照与替代建议 | USE-MIGRATE-007 |
| 输入参数类型 | `boolean` / `choice` / `number` / `environment` / `string` | 仅 `string` | 类型声明被拒绝；是否提示「需改为 string 并在步骤内转换」 | USE-MIGRATE-008 |
| 触发器 types 命名 | `opened` / `synchronize` / `reopened` | `open` / `update` / `reopen` / `merge` | 写 GitHub 命名导致 workflow 不触发；是否静默失败或有提示 | USE-MIGRATE-009 |
| 废弃命令 | `::set-output` / `::set-env` / `::add-path` | 废弃，改用 `ATOMGIT_OUTPUT` 等文件 | 使用旧命令时报错；是否给出替代命令示例 | USE-MIGRATE-010 |

### 1.3 概念差异（文档可发现性）

| 差异项 | GitHub | GitCode | 迁移摩擦点 | 对应 Intent |
|---|---|---|---|---|
| 阶段机制 | 无 stages 概念，仅有 job DAG | 顶层 `stages`（阶段间串行+阶段内并行） | 迁移者不知道需要 stages；文档是否充分解释 | USE-MIGRATE-011 |
| 后处理阶段 | 无顶层 `post`（仅 action 内 post） | 顶层 `post`（默认 `run_always: true`） | 迁移者不知道可用 post；文档是否放在显眼位置 | USE-MIGRATE-011 |

---

## 2. Intent 列表

---

```
意图 ID:    INTENT-USE-001
维度标签:   [usability]
标题:       工作流目录差异报错质量 — .github/workflows 搬运到 GitCode 时的路径指引

风险点:     迁移者直接复制 GitHub workflow 到 .github/workflows/，GitCode 不识别该目录，导致 workflow 完全不运行且无直观报错。
            若系统仅静默忽略，用户会困惑「为什么 push 了但没触发流水线」。
预期系统行为: 当仓库存在 .github/workflows/ 下的 .yml/.yaml 文件但不存在 .gitcode/workflows/ 下的文件时，系统应在某处给出提示；
            更理想的是在解析阶段明确报错「未找到 workflow 文件，GitCode 使用 .gitcode/workflows/ 目录」。
Oracle 来源: GitCode规格（workflow-file-location-structure.md）+ GitHub行为（.github/workflows/）

验证要点:
  - [正向] 在 .gitcode/workflows/ 放置 workflow 文件后正常触发
  - [负向] 仅存在 .github/workflows/ 时不应静默无任何提示（至少应在 Actions 页面或运行日志中提示无 workflow 文件）
  - [非功能] 报错/提示信息中应包含「.gitcode/workflows」字样

可理解性判据: 错误信息必须同时包含「.github/workflows」与「.gitcode/workflows」对照字样，并指明「GitCode 使用 .gitcode/workflows 目录存放工作流文件」；若仅为泛化提示，视为不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; COMPAT-NOTES.md §1; parity-matrix.md「工作流文件目录」
```

---

```
意图 ID:    INTENT-USE-002
维度标签:   [usability, compatibility]
标题:       上下文命名差异报错质量 — github.* 表达式失效时是否指明 atomgit.* 替代

风险点:     迁移者沿用 GitHub 的 `${{ github.ref }}`、`${{ github.sha }}` 等表达式，在 GitCode 中这些上下文对象不存在。
            若报错仅说「未知上下文 github」而不提示「GitCode 使用 atomgit」，用户需要翻文档才能发现前缀差异。
预期系统行为: YAML 解析或表达式求值阶段遇到不存在的上下文时，报错应明示该上下文在 GitCode 中的对应名称（如 github → atomgit）。
Oracle 来源: GitCode规格（syntax-reference/context.md）+ GitHub行为（contexts.md）

验证要点:
  - [正向] 使用 ${{ atomgit.ref }} 时表达式正常求值
  - [负向] 使用 ${{ github.ref }} 时不应静默求值为空字符串或静默失败（应给出解析/求值错误）
  - [非功能] 报错信息中应包含「atomgit」字样并给出替换建议

可理解性判据: 报错信息必须同时出现「github」与「atomgit」字样，并给出「GitCode 使用 atomgit 上下文替代 github」的明确指引；若仅报「unknown context 'github'」而无替换提示，视为不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/context.md; github-reference/reference/contexts.md; COMPAT-NOTES.md §2; parity-matrix.md「上下文对象命名」
```

---

```
意图 ID:    INTENT-USE-003
维度标签:   [usability, compatibility]
标题:       环境变量前缀差异 — Shell 脚本引用 GITHUB_* 空值/报错时的提示质量

风险点:     迁移者的 Shell 脚本中大量引用 `$GITHUB_SHA`、`$GITHUB_OUTPUT` 等环境变量，在 GitCode Runner 中这些变量不存在。
            若脚本未做防御性检查，会导致空值传入下游命令，产生难以定位的 secondary failure。
预期系统行为: 当 Runner 执行 step 中引用未定义的环境变量时， ideally 系统应在日志中给出警告（bash 的 nounset 模式或平台级提示），
            或文档应在迁移指引中给出显式的变量映射表。
Oracle 来源: GitCode规格（runtime-environment-variables.md）+ GitHub行为（workflow-commands.md）

验证要点:
  - [正向] 使用 $ATOMGIT_SHA 时正常取值
  - [负向] 使用 $GITHUB_SHA 时若脚本未设默认值，不应静默继续导致后续命令异常
  - [非功能] 日志中是否出现关于「GITHUB_* 环境变量在 GitCode 中对应为 ATOMGIT_*」的提示或警告

可理解性判据: 若平台在日志中对引用未定义变量给出警告，警告中应包含「ATOMGIT_」前缀提示；更理想的：文档的「迁移指引」或「常见问题」中必须包含 GITHUB_* → ATOMGIT_* 的完整对照表。eval: 是（判断「日志警告是否足够醒目且含有效指引」需主观评判）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/action-development/runtime-environment-variables.md; github-reference/reference/workflow-commands.md; COMPAT-NOTES.md §2
```

---

```
意图 ID:    INTENT-USE-004
维度标签:   [usability, compatibility]
标题:       状态函数括号差异 — success() 语法报错是否提示「GitCode 不带括号」

风险点:     GitHub 的状态函数是 `success()` / `failure()` / `always()` / `cancelled()`（带括号函数调用）。
            GitCode 写 `success` / `failed` / `always` / `cancelled`（无括号）。
            迁移者写 `if: ${{ success() }}` 时会触发语法/求值错误，若报错仅说「unexpected token」而不解释差异，用户难以自行修正。
预期系统行为: 表达式解析器遇到带括号的状态函数时，报错应明确指出「GitCode 状态函数无需括号，请使用 success / failed / always / cancelled」。
Oracle 来源: GitCode规格（syntax-reference/expressions.md）+ GitHub行为（expressions.md）

验证要点:
  - [正向] 使用 `if: ${{ success }}` 时正常求值
  - [负向] 使用 `if: ${{ success() }}` 时不应静默忽略括号（如被解释为函数调用并产生不可预期行为）
  - [非功能] 报错信息中应包含「括号」或「()」相关提示，并给出 GitCode 正确写法

可理解性判据: 报错信息必须包含「success」或「failure」或「状态函数」关键词，并明示「GitCode 状态函数不带括号」；若仅为泛化的「syntax error」或「unexpected token '('」，视为不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/expressions.md; github-reference/reference/expressions.md; COMPAT-NOTES.md §3; parity-matrix.md「状态函数括号语法」
```

---

```
意图 ID:    INTENT-USE-005
维度标签:   [usability, compatibility]
标题:       permissions 权限域命名差异 — GitHub 命名被使用时报错是否给出 GitCode 对照

风险点:     GitHub 的 permissions 域为 `contents` / `pull-requests` / `issues` / `actions` 等；GitCode 为 `repository` / `pr` / `issue` / `note` / `hook`。
            迁移者直接复制 permissions 块后，若系统仅静默忽略未知域或报泛化错误，用户不会意识到是命名差异。
预期系统行为: YAML 校验阶段发现未知的 permissions 域时，报错应列出 GitCode 支持的权限域名称，并提示「GitCode 权限域命名与 GitHub 不同」。
Oracle 来源: GitCode规格（security-permissions/token-permissions.md + workflow-file-location-structure.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 使用 `repository: read` / `pr: write` 等 GitCode 命名时正常生效
  - [负向] 使用 `contents: read` / `pull-requests: write` 等 GitHub 命名时不应静默生效（应被识别为未知域）
  - [非功能] 报错中应列出 GitCode 可用权限域列表（project/pr/issue/note/repository/hook）

可理解性判据: 报错信息必须同时出现「contents」或「pull-requests」等 GitHub 命名与「repository」或「pr」等 GitCode 命名，形成对照；若仅报「unknown permission 'contents'」而无可用列表，视为不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md; gitcode-spec/writing-pipelines/workflow-file-location-structure.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §6; parity-matrix.md「permissions 权限域命名」
```

---

```
意图 ID:    INTENT-USE-006
维度标签:   [usability, compatibility]
标题:       runs-on 标签不匹配时报错质量 — 是否给出三段式标签格式指引

风险点:     GitHub 的 `runs-on: ubuntu-latest` 是单标签或数组；GitCode 是 `{os,arch,flavor}` 三段式或 `default`。
            迁移者写 `runs-on: ubuntu-latest` 后 job 无法调度，若报错只说「无可用 runner」而不解释标签体系差异，用户难以自行修正。
预期系统行为: 当 `runs-on` 标签无匹配 Runner 时，报错应说明「未找到匹配 Runner」，并给出 GitCode 三段式标签格式示例或可用标签列表。
Oracle 来源: GitCode规格（runner-management/selecting-runner-labels.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 使用 `runs-on: {ubuntu-24,x64,small}` 或 `runs-on: default` 时正常调度
  - [负向] 使用 `runs-on: ubuntu-latest` 时不应无限排队或静默卡住
  - [非功能] 报错/提示中应包含「三段式」「{os,arch,flavor}」或「default」等关键词

可理解性判据: 报错信息必须包含「runs-on」或「runner 标签」相关说明，并给出至少一个正确示例（如 `{ubuntu-24,x64,small}` 或 `default`）；若仅报「no runner available」而无格式指引，视为不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/runner-management/selecting-runner-labels.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §7; parity-matrix.md「runs-on 标签体系」
```

---

```
意图 ID:    INTENT-USE-007
维度标签:   [usability, compatibility]
标题:       Action 引用写法差异 — actions/checkout@v4 被使用时报错是否给出迁移指引

风险点:     GitHub 引用 Action 用 `actions/checkout@v4`（带 owner+版本）；GitCode 官方 Action 用短名 `checkout`。
            迁移者写 `uses: actions/checkout@v4` 后，若 GitCode 无法识别，报错是否明示「GitCode 官方 Action 使用短名引用」？
预期系统行为: 当 `uses` 引用的 Action 无法解析时，报错应区分「官方 Action」与「第三方 Action」，并提示 GitCode 官方 Action 的短名引用方式。
Oracle 来源: GitCode规格（writing-pipelines/using-actions.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 使用 `uses: checkout` 时正常拉取官方 Action
  - [负向] 使用 `uses: actions/checkout@v4` 时不应静默失败或报泛化的「Action 不存在」
  - [非功能] 报错中应包含「checkout」短名提示或「GitCode 官方 Action 无需 owner 前缀」说明

可理解性判据: 报错信息必须同时出现「actions/checkout」与「checkout」对照，或给出「GitCode 官方 Action 使用短名」的明确说明。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/using-actions.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §10
```

---

```
意图 ID:    INTENT-USE-008
维度标签:   [usability, compatibility]
标题:       workflow_dispatch inputs 类型限制报错 — 非 string 类型声明是否提示转换指引

风险点:     GitHub 支持 `boolean` / `choice` / `number` / `environment` / `string` 类型；GitCode 仅支持 `string`。
            迁移者复制含 `type: boolean` 或 `type: choice` 的 workflow 后，若报错仅说「type 无效」而不说明「GitCode 仅支持 string，请自行转换」，用户需反复试错。
预期系统行为: YAML 校验阶段遇到非 string 的 input type 时，报错应明确说明「GitCode 仅支持 string 类型输入参数，请在步骤中通过表达式进行类型转换」。
Oracle 来源: GitCode规格（writing-pipelines/configure-triggers.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 使用 `type: string` 时正常通过校验
  - [负向] 使用 `type: boolean` / `type: choice` / `type: number` 时不应静默降级为 string（应给出明确的校验错误）
  - [非功能] 报错中应包含「string」与「类型转换」相关提示

可理解性判据: 报错信息必须包含「GitCode 仅支持 string 类型」或等效说明，并给出「在步骤中使用表达式转换类型」的替代方案。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §9; parity-matrix.md「workflow_dispatch.inputs 类型」
```

---

```
意图 ID:    INTENT-USE-009
维度标签:   [usability, compatibility]
标题:       pull_request types 命名差异 — 使用 GitHub 命名时是否静默失败或有可理解提示

风险点:     GitHub 的 pull_request types 为 `opened` / `synchronize` / `reopened`；GitCode 为 `open` / `update` / `reopen` / `merge`，默认 `[open, reopen, update]`。
            迁移者写 `types: [opened, synchronize]` 后 workflow 不触发，若系统完全静默无提示，用户会以为是触发器本身故障。
预期系统行为: YAML 校验阶段遇到未知的 types 值时，应报错并列出 GitCode 支持的取值范围；或在触发过滤不匹配时给出调试日志。
Oracle 来源: GitCode规格（writing-pipelines/configure-triggers.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 使用 `types: [open, update, reopen]` 时正常触发
  - [负向] 使用 `types: [opened, synchronize]` 时不应静默通过校验并在运行时永远不被触发（应在校验阶段报错）
  - [非功能] 报错/日志中应列出 GitCode 支持的 types 取值列表

可理解性判据: 报错信息必须包含 GitCode 支持的 types 取值（merge, open, reopen, update），并指出「GitHub 的 opened/synchronize/reopened 对应 GitCode 的 open/update/reopen」。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §5
```

---

```
意图 ID:    INTENT-USE-010
维度标签:   [usability, compatibility]
标题:       废弃 workflow 命令报错质量 — ::set-output/::set-env/::add-path 是否给出替代命令

风险点:     GitCode 明确废弃 `::set-output` / `::set-env` / `::add-path`，与 GitHub 演进一致。
            但迁移者的旧 workflow 中仍可能大量使用这些命令；若执行时仅被静默忽略或报泛化错误，用户不会知道应改用 `ATOMGIT_OUTPUT` 等文件协议。
预期系统行为: Runner 执行到废弃命令时，应在日志中输出明确的弃用警告，包含「该命令已废弃」和「请使用 ATOMGIT_OUTPUT/ATOMGIT_ENV/ATOMGIT_PATH 替代」的完整示例。
Oracle 来源: GitCode规格（syntax-reference/workflow-commands.md）+ GitHub行为（workflow-commands.md）

验证要点:
  - [正向] 使用 `echo "key=val" >> $ATOMGIT_OUTPUT` 时正常生效
  - [负向] 使用 `echo "::set-output name=key::val"` 时不应静默生效（应被识别为废弃命令并给出警告或错误）
  - [非功能] 日志警告中应同时包含「废弃」「ATOMGIT_OUTPUT」「ATOMGIT_ENV」「ATOMGIT_PATH」字样

可理解性判据: 报错/警告信息必须包含「已废弃」或「deprecated」字样，并给出至少一条完整的替代命令示例（如 `echo "name=value" >> "$ATOMGIT_OUTPUT"`）。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md; github-reference/reference/workflow-commands.md; COMPAT-NOTES.md §11
```

---

```
意图 ID:    INTENT-USE-011
维度标签:   [usability]
标题:       stages / post 特有概念的文档可发现性 — 迁移者能否在显眼位置找到说明

风险点:     GitCode 特有的 `stages`（阶段间串行）和 `post`（后处理阶段）是 GitHub 没有的概念。
            迁移者若想在 GitCode 上利用这些能力（或避免误用），需要能在文档的「快速入门」「迁移指引」或「常见问题」中快速发现这些差异说明。
            若这些概念仅散落在深层文档页中，迁移者会错过关键能力。
预期系统行为: 文档的「快速入门」「COMPAT-NOTES」或「迁移指引」中，必须在首屏或前 3 个可见章节内提及 `stages` 与 `post` 的存在及与 GitHub 的差异。
Oracle 来源: GitCode规格（workflow-file-location-structure.md / core-concepts/workflow-job-step-action.md / COMPAT-NOTES.md）

验证要点:
  - [正向] 在文档目录的 INDEX / 快速入门 / 迁移指引中搜索「stages」「post」「阶段」「后处理」，确认有可见位置提及
  - [负向] 不应仅在深层子页面提及 stages/post 而与「迁移」主题完全割裂
  - [非功能] 说明中是否给出与 GitHub job DAG 的对比图或对比表

可理解性判据: 文档中关于 stages/post 的说明必须在「迁移相关」或「快速入门」类页面中有入口链接，且说明包含「GitCode 特有」「GitHub 无此概念」等显式差异标注。eval: 是（「显眼位置」「可发现性」需主观评判信息架构是否合理）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; gitcode-spec/core-concepts/workflow-job-step-action.md; COMPAT-NOTES.md §4; parity-matrix.md「stages 阶段机制 / post 后处理阶段」
```

---

```
意图 ID:    INTENT-USE-012
维度标签:   [usability]
标题:       文档残留措辞一致性 — runtime-environment-variables.md 中是否夹带 GitHub 专属变量名

风险点:     COMPAT-NOTES 抓取时观察到 runtime-environment-variables.md 中部分描述文案仍夹带 `GITHUB_ACTION_PATH` 等 GitHub 残留措辞。
            这会导致迁移者困惑：到底应该用 `ATOMGIT_ACTION_PATH` 还是 `GITHUB_ACTION_PATH`？文档自相矛盾。
预期系统行为: 文档中所有环境变量名、上下文名、命令示例必须与 GitCode 实际行为一致，不应出现 `GITHUB_` 前缀的残留（除非是解释差异的对照表）。
Oracle 来源: GitCode规格（runtime-environment-variables.md）

验证要点:
  - [正向] 文档中所有独立的环境变量示例均使用 `ATOMGIT_` 前缀
  - [负向] 正文中不应出现未标注为「GitHub 对照」的 `GITHUB_ACTION_PATH`、`GITHUB_ENV` 等残留措辞
  - [非功能] 若出现对照表，必须明确标注「GitHub 写法」与「GitCode 写法」

可理解性判据: 对 runtime-environment-variables.md 全文进行字符串扫描：独立出现的 `GITHUB_` 前缀（非引用、非对照表场景）数量应为 0。eval: 否（字符串匹配可判定）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/action-development/runtime-environment-variables.md; COMPAT-NOTES.md §2 注
```

---

```
意图 ID:    INTENT-USE-013
维度标签:   [usability, compatibility]
标题:       runner.os 支持平台文档声明与实际一致性

风险点:     GitCode 的 runner 上下文文档写 `runner.os` 可能值为 `Linux`, `Windows`, `macOS`（与 GitHub 一致）。
            但 COMPAT-NOTES 指出目前实际仅提供 Linux（ubuntu/euler）。若文档声明三平台而实际只有 Linux，
            迁移者写 `runs-on: windows-latest` 或 `if: runner.os == 'Windows'` 会失败，且文档未如实管理期望。
预期系统行为: 文档中 `runner.os` 的可取值应与实际可用的 Runner 镜像平台严格一致；未支持的平台不应出现在文档中或必须标注「即将支持」。
Oracle 来源: GitCode规格（syntax-reference/context.md / runner-management/）+ 实际运行行为

验证要点:
  - [正向] 使用 Linux Runner 时 `runner.os` 返回 `Linux`
  - [负向] 若 Windows/macOS Runner 实际不可用，文档中不应声明其支持
  - [非功能] 文档中 runner.os 的说明页是否标注「当前仅支持 Linux」

可理解性判据: 若实际仅有 Linux Runner，文档必须在 `runner.os` 说明旁附加「当前仅 Linux 可用，Windows/macOS 待定」等显式标注。eval: 是（判断「是否足够醒目」需主观评判排版与标注方式）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/context.md; gitcode-spec/runner-management/; COMPAT-NOTES.md §7
```

---

```
意图 ID:    INTENT-USE-014
维度标签:   [usability]
标题:       vars 上下文文档与样本注释矛盾澄清

风险点:     workflow-samples 的 cann/ops-nn_action.yml 样本注释提到「含 vars 上下文（已知不支持 #11）」，
            但 gitcode-spec/syntax-reference/context.md 明确列出了 `vars` 上下文并给出使用示例。
            文档与样本之间出现矛盾，迁移者不知道该信谁。
预期系统行为: `vars` 上下文要么实际可用且文档与样本一致支持，要么实际不可用且文档应下架相关说明。
Oracle 来源: GitCode规格（syntax-reference/context.md）+ workflow-samples/README.md

验证要点:
  - [正向] 若 vars 实际可用，文档示例应能正常运行；样本注释应移除「已知不支持」
  - [负向] 若 vars 实际不可用，文档中不应出现 vars 上下文的使用示例
  - [非功能] 矛盾信息的存在本身就是文档一致性问题

可理解性判据: 文档与样本对同一能力（vars 上下文）的声明必须一致；不一致即视为可理解性缺陷。eval: 否（布尔判定：文档说支持 vs 样本说不支持 = 矛盾）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/context.md; workflow-samples/README.md（cann/ops-nn_action.yml 注释）
```

---

```
意图 ID:    INTENT-USE-015
维度标签:   [usability, compatibility]
标题:       paths 300 文件上限差异是否在文档与行为中一致且明示

风险点:     GitHub 的 paths 过滤基于 diff，有 1,000 commits / 3,000 files 阈值（ workflow-syntax.md ）。
            GitCode 声明「paths 匹配前 300 个变更文件，超出部分不参与匹配」。
            若迁移者的大变更（>300 files）workflow 在 GitCode 上因该限制未触发，而文档未在显眼位置说明，
            用户会困惑「同样的 push 在 GitHub 能触发，在 GitCode 不触发」。
预期系统行为: 文档必须在 paths 过滤说明页（configure-triggers.md）的显眼位置标注「300 文件上限」差异；
            若某次 push 超出 300 文件且未触发，调试日志中应提示「paths 过滤超出文件上限」。
Oracle 来源: GitCode规格（configure-triggers.md）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 变更文件数 <=300 时 paths 过滤正常生效
  - [负向] 变更文件数 >300 时，系统不应静默跳过（应在调试日志或文档中明示上限）
  - [非功能] 文档中「paths」章节的顶部或紧邻位置是否有「300 文件上限」提示

可理解性判据: 文档 configure-triggers.md 中「paths / paths-ignore」说明必须在首段或独立的「注意」块中写明「匹配前 300 个变更文件」；若仅在页面底部或深层子段落提及，视为可理解性不合格。eval: 是（「显眼位置」需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §5; parity-matrix.md「paths 匹配上限」
```

---

```
意图 ID:    INTENT-USE-016
维度标签:   [usability, security]
标题:       secret 日志脱敏绕过风险 — 文档自承行为与实际是否一致

风险点:     GitCode 文档（using-secrets.md）自承 `echo "${{ secrets.X }}"` 可能绕过脱敏。
            若文档写了该风险但实际已修复（不再绕过），则文档在制造不必要的恐慌；
            若实际确实可绕过但文档未给出缓解建议，则用户缺乏 actionable 指引。
预期系统行为: 文档描述的风险必须与实际行为一致；若确实存在绕过，文档应给出「不要在 run 中直接 echo secrets」的可操作缓解建议。
Oracle 来源: GitCode规格（security-permissions/using-secrets.md）+ 实际运行行为

验证要点:
  - [正向] 正常引用 secrets 时日志中应显示为 `***`
  - [负向] 若 `echo "${{ secrets.X }}"` 确实可绕过脱敏，文档应明确建议「改用环境变量注入而非直接 echo」
  - [非功能] 文档中的风险提示段落是否包含「如何改」的可操作建议

可理解性判据: 若文档声明存在绕过风险，必须同时给出「正确写法」与「错误写法」的代码示例对比；仅有风险声明而无缓解建议的，视为可理解性不合格。eval: 是（「缓解建议是否充分且可操作」需主观评判）。

优先级线索: RISK-SEC-01
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md; parity-matrix.md「secrets 日志脱敏」
```

---

```
意图 ID:    INTENT-USE-017
维度标签:   [usability]
标题:       日志按 step 时间线组织的清晰度与可读性

风险点:     当 workflow 含多 stage / 多 job / 多 step 时，日志若层次混乱、时间戳缺失、step 边界不清，
            调试者难以快速定位失败 step。尤其 GitCode 的 stages 机制增加了日志层级深度。
预期系统行为: 每个 job 的日志按 step 顺序组织，每条日志行前缀包含时间戳和 step 编号；长输出 step 支持折叠；stage 边界清晰可见。
Oracle 来源: GitCode规格（running-pipelines/view-job-logs.md）

验证要点:
  - [正向] 日志面板中 step 按定义顺序排列，step 名称与 workflow 定义中的 `name` 一致
  - [正向] 日志行包含时间戳前缀
  - [非功能] 长输出 step 默认折叠，点击后展开不卡顿；不同 stage 的 job 日志在 UI 上有明确的 stage 分组标识

可理解性判据: 在 UI 上，用户能在 3 秒内定位到失败的 step（通过视觉层级、颜色或状态图标区分）；日志下载文件为 UTF-8 编码且本地打开无乱码。eval: 是（「3 秒内定位」「视觉层级清晰度」需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/view-job-logs.md; testing-focus.md §9
```

---

```
意图 ID:    INTENT-USE-018
维度标签:   [usability]
标题:       日志搜索/下载/关键词高亮的交互可用性

风险点:     view-job-logs.md 声称支持日志搜索（关键词高亮）与下载。若搜索功能仅支持简单子串匹配、无正则、无大小写选项，
            或下载的日志文件超大（>100MB）时浏览器崩溃，都会严重影响调试体验。
预期系统行为: 日志搜索支持关键词高亮、大小写敏感选项；下载的日志文件为纯文本格式、编码 UTF-8、大文件可流式下载不崩溃。
Oracle 来源: GitCode规格（running-pipelines/view-job-logs.md）

验证要点:
  - [正向] 在日志面板输入 "Error" / "fatal" 后，匹配行被高亮显示
  - [正向] 点击「下载日志」后获得完整的 UTF-8 编码文本文件
  - [非功能] 搜索响应时间 < 2s；下载 50MB 以上日志时浏览器/页面不崩溃

可理解性判据: 搜索框需在日志面板顶部常驻可见，高亮颜色与背景对比度 >= 3:1（WCAG 基础可访问性）；下载按钮文案明确为「下载日志」或「Download logs」，不可使用模糊图标无文字说明。eval: 是（「可访问性对比度」「交互流畅度」需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/view-job-logs.md; testing-focus.md §9
```

---

```
意图 ID:    INTENT-USE-019
维度标签:   [usability]
标题:       运行状态回写可读性 — Commits 页面与 PR Checks 标签页的状态徽标

风险点:     开发者习惯通过 commit 列表右侧的状态徽标或 PR 的 Checks 标签页快速判断构建结果。
            若状态徽标缺失、延迟过高（>30s）、状态语义不一致（如 GitCode 的「跳过」与 GitHub 的「neutral」混淆），
            会导致评审人误判代码质量。
预期系统行为: 每次 workflow 运行完成后，状态徽标应及时（<30s）回写到 Commits 页面和 PR Checks 页；状态图标（成功/失败/运行中/取消/跳过）语义清晰、颜色对比度高。
Oracle 来源: GitCode规格（running-pipelines/view-run-results.md）+ GitHub行为（状态回写语义）

验证要点:
  - [正向] workflow 运行完成后，Commits 页面出现对应的状态徽标
  - [正向] PR 页面的 Checks 标签页汇总所有相关运行结果
  - [非功能] 从运行完成到徽标刷新延迟 < 30s；跳过状态有独立的图标/颜色（不与成功/失败混淆）

可理解性判据: 状态徽标在 Commits 列表中尺寸 >= 16x16px，颜色含义符合行业惯例（绿=成功、红=失败、黄=运行中、灰=跳过/取消）；鼠标悬停徽标时显示 tooltip，包含 workflow 名称与简要状态。eval: 是（视觉可读性需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/running-pipelines/view-run-results.md; testing-focus.md §9
```

---

```
意图 ID:    INTENT-USE-020
维度标签:   [usability]
标题:       ATOMGIT_STEP_SUMMARY Markdown 渲染质量与可读性

风险点:     步骤摘要（step summary）是调试体验的重要组成：测试报告、构建结果、覆盖率等常以 Markdown 表格/列表形式写入 summary。
            若 GitCode 的 summary 渲染不支持表格、代码块、emoji，或渲染后样式错乱，会严重降低信息可读性。
预期系统行为: `ATOMGIT_STEP_SUMMARY` 写入的 Markdown 内容在运行详情页正确渲染为 HTML；支持表格、代码块、列表、粗体/斜体等常用语法。
Oracle 来源: GitCode规格（syntax-reference/workflow-commands.md + runtime-environment-variables.md）

验证要点:
  - [正向] 写入标准 Markdown 表格后，运行详情页显示为结构化表格
  - [正向] 写入代码块（```bash）后显示为等宽字体代码块
  - [非功能] 表格列宽自适应，不出现横向溢出不可读的情况

可理解性判据: Markdown 表格必须有表头样式区分（背景色或粗体），代码块必须有语法高亮或至少等宽背景；若渲染结果与 GitHub Actions 的 step summary 视觉风格差异大，需评估是否影响迁移者习惯。eval: 是（「渲染质量」「视觉可读性」需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md; gitcode-spec/action-development/runtime-environment-variables.md; parity-matrix.md「ATOMGIT_STEP_SUMMARY」
```

---

```
意图 ID:    INTENT-USE-021
维度标签:   [usability]
标题:       workflow 命令 ::error:: / ::warning:: 的注解生成与关联可读性

风险点:     GitHub Actions 支持 `::error file=...,line=...::message` 和 `::warning::` 命令，
            可在 PR 的 Files changed 页面或 commit 上生成行级 annotation，极大提升代码检查类 workflow 的可理解性。
            GitCode 文档中未明确提及是否支持同等 workflow 命令及 annotation 回写。
            若不支持但文档未说明，迁移者的 lint / code-check workflow 会丢失行级报错定位能力。
预期系统行为: 若支持 `::error::` / `::warning::` / `::notice::` 命令，则 annotation 应正确回写到 PR / commit 的对应行；
            若不支持，文档应在「与 GitHub 的差异」中显式说明。
Oracle 来源: GitCode规格（文档未明确）+ GitHub行为（workflow-commands.md）

验证要点:
  - [正向] 若支持，step 输出 `::error file=src/main.js,line=10::Missing semicolon` 后，PR 页面出现对应行的 error annotation
  - [负向] 若不支持，不应静默忽略（至少应在日志中保留原始命令文本）
  - [非功能] annotation 的 UI 展示是否包含文件路径、行号、错误信息，且可点击跳转到代码

可理解性判据: 若支持 annotation，错误 annotation 在 PR 页面必须包含准确的文件路径、行号、错误信息，且颜色为红色（warning 为黄色）；若不支持，文档的 COMPAT-NOTES 或「差异说明」中必须列出「GitHub 的 ::error:: / ::warning:: annotation 在 GitCode 中暂未支持」。eval: 是（annotation UI 的可理解性需主观评判）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-commands.md; gitcode-spec/syntax-reference/workflow-commands.md（未提及 annotation）; testing-focus.md §9
```

---

```
意图 ID:    INTENT-USE-022
维度标签:   [usability]
标题:       YAML 语法/必填字段缺失报错的行号与可操作性

风险点:     当 workflow YAML 存在缩进错误、必填字段缺失、类型不匹配时，解析报错的质量直接决定修复效率。
            若报错仅说「YAML 解析失败」而不给文件路径、行号、具体字段名，用户只能盲猜。
预期系统行为: YAML 解析失败时，报错必须包含：文件名、出错行号、列号、预期类型/字段与实际值的对照说明。
Oracle 来源: GitCode规格（workflow-file-location-structure.md）+ 通用可诊断性启发式

验证要点:
  - [正向] 缺少必填字段 `on` 时，报错指出「缺少必填字段 'on'」
  - [正向] 缩进错误时，报错指出具体的行号与列号
  - [非功能] 报错中是否给出 YAML 片段示例说明正确写法

可理解性判据: 报错信息必须同时包含「字段名」「所在行号」「正确写法示例」三项中的至少两项；仅有泛化「YAML parse error」而无定位信息的，视为可理解性不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; testing-focus.md §1
```

---

```
意图 ID:    INTENT-USE-023
维度标签:   [usability, compatibility]
标题:       未知/不支持字段处理的报错信息质量

风险点:     parity-matrix.md 标记「未知/不支持字段处理」为 ❓ 状态。文档未明确降级方式。
            若 GitCode 遇到未知字段时静默忽略，迁移者不会知道某字段未生效（如误用 GitHub 的 `run-name`）；
            若报错，报错质量决定了用户能否快速找到替代方案。
预期系统行为: 遇到未知/不支持的字段时，系统应在 YAML 校验阶段给出警告或错误，指明「字段 X 在当前版本不支持」，并给出替代建议（若有）。
Oracle 来源: GitCode规格（多处未明确）+ GitHub行为（workflow-syntax.md）

验证要点:
  - [正向] 对已知支持的字段，正常通过校验
  - [负向] 对未知字段（如 GitHub 的 `run-name`、GitCode 未实现的 `jobs.<id>.container`）不应静默忽略
  - [非功能] 报错/警告中是否包含字段名、文件路径、行号

可理解性判据: 对未知字段的提示必须包含「字段名」和「不支持/unknown」字样；若能识别该字段为 GitHub 特有（如 `run-name`），提示中应追加「该字段为 GitHub Actions 特有，GitCode 暂不支持」。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   parity-matrix.md「未知/不支持字段处理」; github-reference/reference/workflow-syntax.md; testing-focus.md §1
```

---

```
意图 ID:    INTENT-USE-024
维度标签:   [usability, compatibility]
标题:       表达式语法错误（非法上下文/函数）的报错信息质量

风险点:     表达式 `${{ }}` 中的语法错误（如引用不存在的上下文属性、拼写错误的函数名、括号不匹配）是常见错误来源。
            若求值失败时报错仅说「表达式错误」而不给出具体表达式原文和位置，用户难以定位。
预期系统行为: 表达式求值失败时，报错必须包含：原始表达式字符串、错误类型（如 undefined property / unknown function / syntax error）、建议修正方向。
Oracle 来源: GitCode规格（syntax-reference/expressions.md）+ GitHub行为（expressions.md）

验证要点:
  - [正向] 合法表达式正常求值
  - [负向] 非法表达式（如 `${{ atomgit.nonexistent_property }}`、`${{ unknownFunc() }}`）不应静默求值为空字符串
  - [非功能] 报错中是否包含原始表达式字符串和错误位置

可理解性判据: 报错信息必须包含出错的原始表达式（或截断后的前 50 字符）和错误类型说明；若错误是「未知上下文属性」，应提示「请检查上下文名称和属性名拼写」。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/syntax-reference/expressions.md; github-reference/reference/expressions.md; testing-focus.md §1
```

---

```
意图 ID:    INTENT-USE-025
维度标签:   [usability]
标题:       Runner 标签无匹配时的报错信息质量

风险点:     当 `runs-on` 指定的标签组合无可用 Runner 时，job 会处于 queued 状态或失败。
            若报错仅说「无可用 runner」而不列出用户指定的标签和平台实际支持的标签/资源池，
            用户无法判断是标签拼写错误还是资源池容量不足。
预期系统行为: 当 Runner 调度失败时，报错/提示应包含：用户指定的标签列表、当前仓库/组织可用的 Runner 类型或资源池列表、调度失败原因（无匹配 vs 容量不足）。
Oracle 来源: GitCode规格（runner-management/selecting-runner-labels.md）

验证要点:
  - [正向] 标签匹配成功时 job 正常调度到 Runner
  - [负向] 标签完全不匹配时，不应无限 queued 且无提示（应在合理超时后失败并给出原因）
  - [非功能] 错误信息中是否包含用户指定的标签文本

可理解性判据: 报错信息必须包含用户指定的 `runs-on` 标签原文；若因容量不足排队，应提示「当前无空闲 Runner，正在排队」而非「无可用 runner」；若因标签不匹配，应提示「未找到匹配标签的 Runner，可用标签包括：...」。eval: 否（字符串匹配可判定）。

优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   gitcode-spec/runner-management/selecting-runner-labels.md; testing-focus.md §4
```

---

```
意图 ID:    INTENT-USE-026
维度标签:   [usability]
标题:       workflow_call 嵌套超过 2 层时的报错清晰度

风险点:     GitCode 明确限制 `workflow_call` 嵌套最多 2 层。迁移者或复杂 workflow 作者可能无意中超限。
            若报错仅说「调用失败」而不说明「嵌套层数超过上限（最大 2 层）」，用户会误以为是 reusable workflow 本身有 bug。
预期系统行为: 当 reusable workflow 尝试调用第 3 层嵌套时，系统应在解析或调度阶段报错，明确说明「workflow_call 嵌套层数超过 GitCode 上限 2 层」。
Oracle 来源: GitCode规格（writing-pipelines/configure-triggers.md）

验证要点:
  - [正向] 1 层和 2 层嵌套调用正常执行
  - [负向] 第 3 层嵌套调用不应静默失败或卡死
  - [非功能] 报错中是否包含「2 层」「嵌套」「workflow_call」关键词

可理解性判据: 报错信息必须包含「workflow_call」「嵌套」「2 层」「上限」等关键词中的至少两项；若仅报「调用失败」或「无法解析 reusable workflow」，视为可理解性不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; parity-matrix.md「workflow_call 嵌套层数」
```

---

```
意图 ID:    INTENT-USE-027
维度标签:   [usability]
标题:       并发控制 max 超出 1-5 范围时的报错信息

风险点:     GitCode 的 `concurrency.max` 范围为 1-5。若用户写 `max: 10` 或 `max: 0`，
            报错是否给出有效范围？若仅说「配置错误」，用户不知道上限是 5。
预期系统行为: YAML 校验阶段发现 `concurrency.max` 超出 1-5 范围时，报错应明确说明「max 取值范围应为 1-5」。
Oracle 来源: GitCode规格（workflow-file-location-structure.md）

验证要点:
  - [正向] `max: 1` 至 `max: 5` 正常通过校验
  - [负向] `max: 0` / `max: 10` / `max: -1` 不应静默截断为边界值（应报错）
  - [非功能] 报错中是否包含「1」「5」「范围」等关键词

可理解性判据: 报错信息必须包含有效范围「1-5」或「1 到 5」；若仅报「invalid concurrency configuration」而无范围说明，视为可理解性不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; parity-matrix.md「concurrency.max」
```

---

```
意图 ID:    INTENT-USE-028
维度标签:   [usability, security]
标题:       Secret 名称规则违规的报错质量

风险点:     GitCode 规定 Secret 名称不得以 `ATOMGIT_` 开头、不得以数字开头、仅允许大写字母/数字/下划线。
            若用户在 workflow 中引用违规名称（如 `${{ secrets.ATOMGIT_TOKEN }}` 或 `${{ secrets.1SECRET }}`），
            报错是否明确说明命名规则？若仅说「Secret 不存在」，用户可能以为是 Secret 未配置。
预期系统行为: 引用违规名称时，系统应在 YAML 校验或运行时给出明确的命名规则提示，区分「名称违规」与「未配置 Secret」。
Oracle 来源: GitCode规格（security-permissions/using-secrets.md）

验证要点:
  - [正向] 合法名称（如 `PROD_KEY`）正常引用
  - [负向] 以 `ATOMGIT_` 开头的名称不应被允许创建或引用（应给出规则错误）
  - [非功能] 报错中是否包含「Secret 名称规则」「大写字母/数字/下划线」「不得以 ATOMGIT_ 开头」等提示

可理解性判据: 报错信息必须包含「Secret 名称规则」或「命名格式」相关说明，并列出允许字符（大写字母、数字、下划线）；若仅报「Secret not found」而不区分「名称违规」与「未配置」，视为可理解性不合格。eval: 否（字符串匹配可判定）。

优先级线索: RISK-SEC-01
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md
```

---

## 3. 统计摘要

| 分类 | 数量 | 需 llm_assisted 数量 |
|---|---|---|
| 迁移摩擦类 | 11 条 | 2 条（USE-003 环境变量警告醒目度、USE-011 文档可发现性） |
| 文档一致性类 | 5 条 | 3 条（USE-013 runner.os 平台标注醒目度、USE-015 paths 300 上限显眼位置、USE-016 secret 脱敏缓解建议充分性） |
| 调试体验类 | 5 条 | 5 条（USE-017 日志清晰度、USE-018 搜索交互、USE-019 状态徽标可读性、USE-020 Markdown 渲染、USE-021 annotation 可读性） |
| 错误信息质量类 | 7 条 | 0 条 |
| **合计** | **28 条** | **10 条** |

### 按优先级线索分布
- 关联 RISK-USE-01（迁移报错不指明差异）：13 条
- 关联 RISK-COMPAT-01（默认值/差异致行为不同）：13 条
- 关联 RISK-SEC-01（安全相关易用性）：2 条

### 跨维度分布
- 纯 usability：18 条
- usability + compatibility：9 条
- usability + security：2 条

---

## 4. 输入版本标注

| 输入文件 | 版本/日期 | 备注 |
|---|---|---|
| phase01/baseline/parity-matrix.md | 2026-07-21 基线 | 能力对标表 |
| phase01/baseline/risk-register.md | 2026-07-21 基线 | 风险项模板 |
| phase01/inputs/gitcode-spec/COMPAT-NOTES.md | 2026-07-20 抓取 | 差异速记 |
| phase01/inputs/gitcode-spec/syntax-reference/ | 2026-07-20 抓取 | 表达式、上下文、workflow 命令 |
| phase01/inputs/gitcode-spec/writing-pipelines/ | 2026-07-20 抓取 | 触发器、workflow 结构、Action 引用 |
| phase01/inputs/gitcode-spec/running-pipelines/ | 2026-07-20 抓取 | 日志、运行结果 |
| phase01/inputs/gitcode-spec/security-permissions/ | 2026-07-20 抓取 | Secret、Token 权限、PR 安全 |
| phase01/inputs/gitcode-spec/runner-management/ | 2026-07-20 抓取 | Runner 标签 |
| phase01/inputs/gitcode-spec/core-concepts/ | 2026-07-20 抓取 | workflow-job-step-action |
| phase01/inputs/github-reference/reference/ | 2026-07-20 抓取 | GitHub 语法、表达式、上下文对照 |
| phase01/inputs/business-context/README.md | 2026-07-21 | ⚠️ 无实际迁移规模/改造点数据 |
| phase01/inputs/workflow-samples/README.md | 2026-07-21 | ⚠️ 无真实样本 YAML 内容作迁移素材 |
